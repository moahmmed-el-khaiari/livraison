package ma.simo.order_service.Mapper;

import ma.simo.order_service.Dto.request.CreateOrderRequest;
import ma.simo.order_service.Dto.response.OrderResponse;
import ma.simo.order_service.entity.Order;
import ma.simo.order_service.entity.OrderItem;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

public final class OrderMapper {

    private OrderMapper() {}

    // CreateOrderRequest -> Order (entity)
    public static Order toEntity(CreateOrderRequest req) {

        Order order = Order.builder()
                .customerId(req.customerId())
                .status("CREATED")
                .orderNumber(generateOrderNumber())
                .createdAt(Instant.now())
                .updatedAt(Instant.now())
                .totalAmount(BigDecimal.ZERO) // sera recalculé après
                .build();

        List<OrderItem> items = req.items().stream()
                .map(i -> OrderItemMapper.toEntity(i, order))
                .toList();

        order.setItems(items);

        BigDecimal totalAmount = items.stream()
                .map(OrderItem::getLineTotal)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        order.setTotalAmount(totalAmount);

        return order;
    }

    // Order (entity) -> OrderResponse (DTO)
    public static OrderResponse toResponse(Order order) {

        List<OrderResponse.Item> items = (order.getItems() == null)
                ? List.of()
                : order.getItems().stream().map(OrderItemMapper::toResponse).toList();

        return new OrderResponse(
                order.getId(),
                order.getOrderNumber(),
                order.getCustomerId(),
                order.getStatus(),
                order.getTotalAmount(),
                order.getTrackingNumber(),
                order.getCreatedAt(),
                order.getUpdatedAt(),
                items
        );
    }

    private static String generateOrderNumber() {
        return "ORD-" + System.currentTimeMillis();
    }
}
