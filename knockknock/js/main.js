const $login = $('#login')
const $interest = $('#interest')
const $waiting = $('#waiting')

const $leftContent = $(".leftContent")
const $rightContent = $(".rightContent")
const $centerContent = $(".centerContent")
const $title = $(".title")
const $date = $(".date")

const Social = Object.freeze({
  
})
const Method = Object.freeze({
    GET: 'GET', POST: 'POST', PUT: 'PUT', DELETE: 'DELETE'
})

const HttpStatus = Object.freeze({
    OK: 200, MOVED_PERMANENTLY: 301, NO_CONTENT: 204, CREATED: 201
})

const messaging = (function () {
    const config = Object.freeze({
        apiKey: "AIzaSyB5h1dtyUXyYroO4ZengUlSKCa93-WoRnU",
        authDomain: "jarvis-77f82.firebaseapp.com",
        databaseURL: "https://jarvis-77f82.firebaseio.com",
        projectId: "jarvis-77f82",
        storageBucket: "jarvis-77f82.appspot.com",
        messagingSenderId: "172501072688",
        appId: "1:172501072688:web:17b57e04673ab8351ba6f5",
        measurementId: "G-WJ48JZCEDP"
    })

    firebase.initializeApp(config)

    return firebase.messaging()
})()

// const basieUrl = "http://ec2-15-165-118-201.ap-northeast-2.compute.amazonaws.com:8080/kk/"
const basieUrl = "http://localhost:8080/kk/"

var prevAjax = null
var checkingData = null

$(document).ready(function () {

    $(".socialLogin").on('click', function (event) {
        socialLogin(Social[this.getAttribute('data-site')])
    })

    $("#checkBtn").on('click', function (event) {
        $title.text("잠시만 기다려주세요!")
        $date.text("Sorry! Just a moment plz.")
        resetContent()
        getCurrentTabUrl(url => new AjaxBuilder().url("check").method(Method.GET).data({url: encodeURIComponent(url)})
            .success((data, status, xhr) => {
                if(xhr.status === HttpStatus.OK){
                    pickMe(data)
                } else {
                    $title.text("지원하지 않는 쇼핑몰 입니다!")
                    $date.text("원하시는 상품명을 입력해주세요...")
                    $centerContent.html('<input type="text" class="wantedTitle"><span class="naverBtn">찾기</span>')
                }
            })
            .build())
    })

    $(".content").on('click', '.pickBtn', function (event) {
        checkingData.wantedPrice = uncomma(document.getElementsByClassName('wantedPrice')[0].value)
        let pick = {product: {title: checkingData.title, price: checkingData.price, fee: checkingData.fee, link: checkingData.link, image: checkingData.image}, wantedPrice: checkingData.wantedPrice}
        new AjaxBuilder().method(Method.POST).url("pick").data(JSON.stringify(pick)).success(status=>status===HttpStatus.CREATED ? alert("Pick 완료!") : alert("이미 등록되어있습니다!")).build()
    }).on('keyup', '.wantedPrice', function (event) {
        inputNumberFormat(this)
    }).on('click', '.productTitle', function (event) {
        new AjaxBuilder().method(Method.GET).url("click").data({no: this.getAttribute("data-no")}).build()
    }).on('click', '.naverBtn', event => {
        $waiting.css('display', 'block')
        let title = document.getElementsByClassName('wantedTitle')[0].value
        setTimeout(function () {
            new AjaxBuilder().method(Method.GET).url("navershopping/"+title).success(data=>pickMe(data)).build()
        }, 500)
    }).on('click', '#logout', event =>
        new AjaxBuilder().url("logout").method(Method.GET).build()
    ).on('click', '#interestBtn', event =>
        //내 관심사 가져와서 채워넣기
        $interest.css('display', 'block')
    ).on('click', '#pickListBtn', event => {
        $leftContent.html('')
        $rightContent.html('')
        new AjaxBuilder().url("pickList").method(Method.GET).success(list => {
            console.log(list)
            Array.from(list).forEach(item => item.no % 2 == 0 ? appendRightContent("#pickListTemplate", item) : appendLeftContent("#pickListTemplate", item))
        }).build()
    }).on('click', '.dropPick', function (event) {
        let $this = $(this)
        new AjaxBuilder().url("dropPick/"+$this.attr('data-no')).method(Method.DELETE).success(data=>{
            alert("삭제가 완료되었습니다!")
            $this.parents(".container").remove()
        }).build()
    })

    $("#infoSetBtn").on('click', event => {
        resetContent()
        $title.text("")
        $date.text("설정 페이지")
        $centerContent.html("<button id='pickListBtn'>Pick 목록</button><button id='interestBtn'>관심사 설정</button><button id='logout'>로그아웃</button>")
    })


    $("#saveInterestBtn").on('click', event => {
        let interests = new Array();
        $("input:checkbox[name=category]:checked").each((index, item) => interests.push(item.value))
        interests.length > 0 ? new AjaxBuilder().method(Method.PUT).url("updateInterest").data(JSON.stringify(interests)).success(status => $interest.css('display', 'none')).build() : alert('하나 이상 선택해주세요!')
    })

    $("#listBtn").on('click', event =>
        new AjaxBuilder().method(Method.GET).url("list").success(list => {
            let now = new Date()
            let hour = now.getHours()
            $title.text("Knock Knock")
            $date.text(now.toLocaleDateString().replace(/ /gi, '').slice(0, -1) + (hour >= 12 ? ' PM ' + (hour - 12) : ' AM ' + hour) + '시 특가!')
            resetContent()
            Array.from(list).forEach(item => item.no % 2 == 0 ? appendLeftContent("#listTemplate",item) : appendRightContent("#listTemplate", item))
        }).build())

    $("#listBtn").trigger('click')
})

function comma(str) {
    str = String(str);
    return str.replace(/(\d)(?=(?:\d{3})+(?!\d))/g, '$1,');
}

function uncomma(str) {
    str = String(str);
    return str.replace(/[^\d]+/g, '');
}

function inputNumberFormat(obj) {
    obj.value = comma(uncomma(obj.value));
}

function setTemplate(templateName, data) {
    let template = $(templateName).html();
    Mustache.parse(template);
    let rendered = Mustache.render(template, data);

    return rendered
}

function pickScrean(data) {
    $waiting.css('display', 'none')
    data.price = comma(data.price)
    data.fee = data.fee === 0 ? '무료' : comma(data.fee)
    return setTemplate("#pickTemplate", data)
}

function content(template, data) {
    let product = data.product
    product.pno = data.pno
    product.fee = product.fee === 0 ? '무료' : comma(product.fee)
    product.price = comma(product.price)
    return setTemplate(template, product)
}

function pickMe(data) {
    resetContent()
    checkingData = $.extend(true, {}, data)
    $title.text("Pick Me!")
    $date.text("")
    $leftContent.html('<img src="'+data.image+'" style="width: auto; height: 200px;">')
    $rightContent.html(pickScrean((data)))
}

function resetContent() {
    $centerContent.html('')
    $leftContent.html('')
    $rightContent.html('')
}

function appendLeftContent(template, data) {
    $leftContent.append(content(template, data))
}

function appendRightContent(template,data) {
    $rightContent.append(content(template, data))
}

function registerClientToken() {
    messaging.requestPermission()
        .then(() => messaging.getToken())
        .then(token =>
            new AjaxBuilder().method(Method.POST).url("token").data(decodeURIComponent(token)).build()
        )
        .catch(err => console.log("Error Occured" + err))
}

function socialLogin(url) {
    const loginPopup = window.open(url, '_black', 'width=auto, height=auto')

    let interval = window.setInterval(() => {
        if (loginPopup.closed) {
            window.clearInterval(interval)
            registerClientToken()

            //301일시 이동
            new AjaxBuilder().method(Method.GET).url("interestChecking")
                .success(status => status === HttpStatus.MOVED_PERMANENTLY ? $interest.css('display', 'block') : executeAjax(prevAjax)).build()

            $login.css('display', 'none')
        }
    }, 1000);
}

function executeAjax(ajax) {
    $.ajax({
        url: ajax.url,
        type: ajax.method,
        data: ajax.data,
        contentType: "application/json",
        async: false,
        success: function (response, status, xhr) {
            ajax.success(response, status, xhr )
        },
        error: function (error) {
            console.log(error)
            if (ajax.url === basieUrl + 'token') return
            let status = error.responseJSON.status
            prevAjax = ajax
            status === 401 ? $login.css('display', 'block') : console.log("Error :" + status)
        }
    })
}

function getCurrentTabUrl(callback) {
    let queryInfo = {active: true, currentWindow: true}
    chrome.tabs.query(queryInfo, function (tabs) {
        let tab = tabs[0]
        let url = tab.url
        callback(url)
    })
}

class Ajax {
    constructor(url, method, data, success) {
        this.url = url;
        this.method = method;
        this.data = data;
        this.success = success;
    }
}

class AjaxBuilder {

    constructor() {
        this.ajax = new Ajax()
    }

    url(url) {
        this.ajax.url = basieUrl + url
        return this
    }

    method(method) {
        this.ajax.method = method
        return this
    }

    data(data) {
        this.ajax.data = data
        return this
    }

    success(success) {
        this.ajax.success = success
        return this
    }

    build() {
        executeAjax(this.ajax)
        return this.ajax
    }
}
