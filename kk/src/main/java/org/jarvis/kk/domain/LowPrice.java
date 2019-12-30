package org.jarvis.kk.domain;

import javax.persistence.Embeddable;

import org.jarvis.kk.dto.BaseTimeEntity;
import org.jarvis.kk.dto.Product;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * LowPrice
 */
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Embeddable
public class LowPrice extends BaseTimeEntity {

    private Product product;

}