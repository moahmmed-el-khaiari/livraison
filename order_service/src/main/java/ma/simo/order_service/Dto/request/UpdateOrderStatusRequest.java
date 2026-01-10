package ma.simo.order_service.Dto.request;

import jakarta.validation.constraints.NotBlank;

public record UpdateOrderStatusRequest( @NotBlank String status)

{
}
