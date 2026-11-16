import { z } from "zod";

export const FilterParamsSchema = z.object({
  limit: z
    .number()
    .int()
    .default(100)
    .refine((v) => v > 0, { message: "limit must be greater than 0" })
    .refine((v) => v <= 100, { message: "limit must be less than or equal to 100" }),
  offset: z
    .number()
    .int()
    .default(0)
    .refine((v) => v >= 0, { message: "offset must be greater than or equal to 0" }),
  order_by: z
    .enum(["created_at", "updated_at"])
    .default("created_at"),
  tags: z
    .array(z.string())
    .default([]),
});
