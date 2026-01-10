package ma.simo.order_service.Mapper;

import ma.simo.order_service.Dto.request.CreateOrderRequest;
import ma.simo.order_service.Dto.response.OrderResponse;
import ma.simo.order_service.entity.Order;
import ma.simo.order_service.entity.OrderItem;

import java.math.BigDecimal;

public final class OrderItemMapper {

    private OrderItemMapper() {}

    // DTO Item (CreateOrderRequest.Item) -> Entity OrderItem
    public static OrderItem toEntity(CreateOrderRequest.Item dto, Order order) {
        BigDecimal unitPrice = BigDecimal.valueOf(dto.unitPrice());
        BigDecimal lineTotal = unitPrice.multiply(BigDecimal.valueOf(dto.quantity()));

        return OrderItem.builder()
                .productId(dto.productId())
                .productName(dto.productName())
                .unitPrice(unitPrice)
                .quantity(dto.quantity())
                .lineTotal(lineTotal)
                .order(order)
                .build();
    }

    // Entity OrderItem -> DTO OrderResponse.Item
    public static OrderResponse.Item toResponse(OrderItem item) {
        return new OrderResponse.Item(
                item.getId(),
                item.getProductId(),
                item.getProductName(),
                item.getUnitPrice(),
                item.getQuantity(),
                item.getLineTotal()
        );
    }
}
