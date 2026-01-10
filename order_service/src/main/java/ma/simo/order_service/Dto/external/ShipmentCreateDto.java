package ma.simo.order_service.Dto.external;

public record ShipmentCreateDto(String serviceLevel,
                                Double weightKg,
                                AddressDto pickupAddress,
                                AddressDto deliveryAddress
) {
    public record AddressDto(
            String fullName,
            String phone,
            String street,
            String city,
            String zip,
            String country,
            Double lat,
            Double lng
    ) {}
}
