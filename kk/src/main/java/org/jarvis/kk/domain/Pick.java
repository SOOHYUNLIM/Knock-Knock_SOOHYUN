package org.jarvis.kk.domain;

import java.util.Set;

import javax.persistence.AttributeOverride;
import javax.persistence.CollectionTable;
import javax.persistence.Column;
import javax.persistence.ElementCollection;
import javax.persistence.Embedded;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import com.fasterxml.jackson.annotation.JsonBackReference;

import org.jarvis.kk.dto.BaseTimeEntity;
import org.jarvis.kk.dto.Product;

import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Pick
 */
@Getter
@Setter
@NoArgsConstructor
@Entity
@Table(name = "tbl_pick")
public class Pick extends BaseTimeEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer pno;

    @Embedded
    @AttributeOverride(name = "price", column = @Column(name = "currentPrice"))
    private Product product;

    private Integer wantedPrice;

    @JsonBackReference
    @ManyToOne(fetch = FetchType.LAZY)
    private Member member;

    private Boolean state;

    @Column(insertable = false, columnDefinition = "bit default 1")
    private Boolean receipt;

    @ElementCollection(fetch = FetchType.LAZY)
    @CollectionTable(name = "tbl_lowprice", joinColumns = @JoinColumn(name = "pno"))
    private Set<LowPrice> lowPrices;

    @Builder
    public Pick(Member member, Product product, Integer wantedPrice) {
        this.member = member;
        this.product = product;
        this.wantedPrice = wantedPrice;
    }

    public Pick updateReceipt(Boolean receipt) {
        this.receipt = receipt;
        return this;
    }

    public LowPrice OnelowPrice() {
        Integer low = null;
        LowPrice result = null;
        for (LowPrice row : lowPrices) {
            if (low == null) {
                row.getProduct().getPrice();
                result = row;
            }
            if (low > row.getProduct().getPrice())
                result = row;
        }
        return result;
    }
}