import { z } from "zod";

export const ItemSchema = z.object({
  name: z.string(),
  description: z.string().nullable().optional(),
  price: z.number(),
  tax: z.number().nullable().optional(),
});
