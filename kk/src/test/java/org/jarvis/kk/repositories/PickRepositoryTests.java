package org.jarvis.kk.repositories;

import org.jarvis.kk.domain.Member;
import org.jarvis.kk.domain.Pick;
import org.jarvis.kk.dto.Product;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import lombok.extern.slf4j.Slf4j;

/**
 * PickRepositoryTests
 */
@SpringBootTest
@Slf4j
public class PickRepositoryTests {

    @Autowired
    private PickRepository pickRepository;
    @Autowired
    private MemberRepository memberRepository;

    @Test
    public void test(){
        // pickRepository.save(new Pick());
        // Member member = memberRepository.getOne("tjsvndrlskfk@gmail.com");
        // Product product = Product.builder().title("[김나운더키친] 김나운 도가니탕+도가니수육!! 3팩,5팩,10팩 골라담기").build();
        // Pick pick = Pick.builder().member(member).product(product).build();
        // log.info(pickRepository.test(pick).get().getProduct().getTitle());
    }
}