import { z } from "zod";

export const ItemSchema = z.object({
  name: z.string(),
  description: z
    .string()
    .max(300)
    .optional()
    .nullable()
    .describe("The description of the item"),
  price: z
    .number()
    .gt(0)
    .describe("The price must be greater than zero"),
  tax: z.number().optional().nullable(),
});
