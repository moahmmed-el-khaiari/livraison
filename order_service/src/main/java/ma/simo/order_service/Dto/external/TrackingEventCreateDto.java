package ma.simo.order_service.Dto.external;

public record TrackingEventCreateDto(
        String trackingNumber,
        String status,   // CREATED / IN_TRANSIT / DELIVERED...
        String source,   // ORDER_SERVICE / SHIPMENT_SERVICE...
        String city,
        String message,
        Double lat,
        Double lng
) {}
