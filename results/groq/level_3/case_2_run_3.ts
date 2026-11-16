import { z } from "zod";

export const ImageSchema = z.object({
  url: z.string().url(),
  name: z.string(),
});

export const ItemSchema = z.object({
  name: z.string(),
  description: z.string().nullable().optional(),
  price: z.number(),
  tax: z.number().nullable().optional(),
  tags: z.array(z.string()).default([]),
  images: z.array(ImageSchema).nullable().optional(),
});

export const OfferSchema = z.object({
  name: z.string(),
  description: z.string().nullable().optional(),
  price: z.number(),
  items: z.array(ItemSchema),
});
