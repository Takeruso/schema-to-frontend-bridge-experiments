import { z } from "zod";

export const ImageSchema = z.object({
  url: z.string(),
  name: z.string(),
});

export const ItemSchema = z.object({
  name: z.string(),
  description: z.string().nullable().optional(),
  price: z.number(),
  tax: z.number().nullable().optional(),
  tags: z
    .array(z.string())
    .transform((arr) => new Set(arr))
    .default(() => new Set<string>()),
  image: ImageSchema.nullable().optional(),
});

export type Image = z.infer<typeof ImageSchema>;
export type Item = z.infer<typeof ItemSchema>;
