package ma.simo.order_service.service;

import ma.simo.order_service.Dto.request.CreateOrderRequest;
import ma.simo.order_service.Dto.response.OrderResponse;

public interface OrderService {
    OrderResponse createOrder(CreateOrderRequest request);
    OrderResponse getByOrderNumber(String orderNumber);
    OrderResponse updateStatus(String orderNumber, String newStatus);
}
