import { z } from "zod";

const capitalize = (value: string): string =>
  value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();

export const Model = z.object({
  f1: z.string().transform(capitalize),
  f2: z.string().transform(capitalize),
});
