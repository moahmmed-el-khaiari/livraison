package ma.simo.order_service.Dto.request;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

import java.util.Arrays;
import java.util.List;


public record CreateOrderRequest(@NotBlank String customerId,

                                 @NotEmpty @Valid List<Item> items,

                                 @NotNull PickupAddress pickupAddress,
                                 @NotNull DeliveryAddress deliveryAddress,

                                 @NotNull @Min(1) Double weightKg,
                                 @NotBlank String serviceLevel // STANDARD / EXPRESS...
) {


    public record Item(
            @NotBlank String productId,
            @NotBlank String productName,
            @NotNull @Min(1) Integer quantity,
            @NotNull @Min(0) Double unitPrice
    ) {}

    // Adresses simples (on peut aussi les mettre dans dto/external si tu veux)
    public record PickupAddress(
            @NotBlank String fullName,
            @NotBlank String phone,
            @NotBlank String street,
            @NotBlank String city,
            String zip,
            @NotBlank String country,
            Double lat,
            Double lng
    ) {}

    public record DeliveryAddress(
            @NotBlank String fullName,
            @NotBlank String phone,
            @NotBlank String street,
            @NotBlank String city,
            String zip,
            @NotBlank String country,
            Double lat,
            Double lng
    ) {}
}
