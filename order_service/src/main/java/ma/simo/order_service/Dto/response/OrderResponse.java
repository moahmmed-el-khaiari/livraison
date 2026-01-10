package ma.simo.order_service.Dto.response;


import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

public record OrderResponse( String id,
                             String orderNumber,
                             String customerId,
                             String status,
                             BigDecimal totalAmount,
                             String trackingNumber,
                             Instant createdAt,
                             Instant updatedAt,
                             List<Item> items
) {
    public record Item(
            String id,
            String productId,
            String productName,
            BigDecimal unitPrice,
            Integer quantity,
            BigDecimal lineTotal
    ) {}
}
