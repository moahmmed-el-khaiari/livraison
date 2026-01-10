package ma.simo.order_service.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import lombok.RequiredArgsConstructor;
import ma.simo.order_service.Client.ShipmentClient;
import ma.simo.order_service.Client.TrackingClient;
import ma.simo.order_service.Dto.external.ShipmentCreateDto;
import ma.simo.order_service.Dto.external.ShipmentResponseDto;
import ma.simo.order_service.Dto.external.TrackingEventCreateDto;
import ma.simo.order_service.Dto.request.CreateOrderRequest;
import ma.simo.order_service.Dto.response.OrderResponse;
import ma.simo.order_service.Mapper.OrderMapper;
import ma.simo.order_service.Repository.OrderRepository;
import ma.simo.order_service.entity.Order;
import ma.simo.order_service.service.OrderService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
@Service
@RequiredArgsConstructor
public class OrderServiceImpl implements OrderService {

    private final OrderRepository orderRepository;
    private final ShipmentClient shipmentClient;
    private final TrackingClient trackingClient;

    @Override
    @Transactional
    public OrderResponse createOrder(CreateOrderRequest request) {

        // 1) Mapper -> Entity + calcul total
        Order order = OrderMapper.toEntity(request);

        // 2) Persist d'abord (pour avoir l'id si besoin)
        order = orderRepository.save(order);

        // 3) Créer shipment via shipment-service (FastAPI)
        ShipmentCreateDto shipmentPayload = new ShipmentCreateDto(
                request.serviceLevel(),
                request.weightKg(),
                new ShipmentCreateDto.AddressDto(
                        request.pickupAddress().fullName(),
                        request.pickupAddress().phone(),
                        request.pickupAddress().street(),
                        request.pickupAddress().city(),
                        request.pickupAddress().zip(),
                        request.pickupAddress().country(),
                        request.pickupAddress().lat(),
                        request.pickupAddress().lng()
                ),
                new ShipmentCreateDto.AddressDto(
                        request.deliveryAddress().fullName(),
                        request.deliveryAddress().phone(),
                        request.deliveryAddress().street(),
                        request.deliveryAddress().city(),
                        request.deliveryAddress().zip(),
                        request.deliveryAddress().country(),
                        request.deliveryAddress().lat(),
                        request.deliveryAddress().lng()
                )
        );

        ShipmentResponseDto shipment = shipmentClient.createShipment(shipmentPayload);

        // 4) Sauvegarder trackingNumber dans order
        order.setTrackingNumber(shipment.trackingNumber());
        order = orderRepository.save(order);

        // 5) Ajouter le 1er event de tracking (CREATED)
        trackingClient.addEvent(new TrackingEventCreateDto(
                shipment.trackingNumber(),
                "CREATED",
                "ORDER_SERVICE",
                shipment.deliveryAddress() != null ? shipment.deliveryAddress().city() : null,
                "Commande créée, expédition enregistrée.",
                shipment.deliveryAddress() != null ? shipment.deliveryAddress().lat() : null,
                shipment.deliveryAddress() != null ? shipment.deliveryAddress().lng() : null
        ));

        // 6) Retour
        return OrderMapper.toResponse(order);
    }

    @Override
    @Transactional(readOnly = true)
    public OrderResponse getByOrderNumber(String orderNumber) {
        Order order = orderRepository.findByOrderNumber(orderNumber)
                .orElseThrow(() -> new RuntimeException("Order not found: " + orderNumber));
        return OrderMapper.toResponse(order);
    }

    @Override
    @Transactional
    public OrderResponse updateStatus(String orderNumber, String newStatus) {
        Order order = orderRepository.findByOrderNumber(orderNumber)
                .orElseThrow(() -> new RuntimeException("Order not found: " + orderNumber));

        order.setStatus(newStatus);
        order = orderRepository.save(order);

        // Optionnel : pousser event tracking si tu veux
        if (order.getTrackingNumber() != null) {
            trackingClient.addEvent(new TrackingEventCreateDto(
                    order.getTrackingNumber(),
                    newStatus,          // si tu alignes tes statuts
                    "ORDER_SERVICE",
                    null,
                    "Statut commande mis à jour: " + newStatus,
                    null,
                    null
            ));
        }

        return OrderMapper.toResponse(order);
    }
}
