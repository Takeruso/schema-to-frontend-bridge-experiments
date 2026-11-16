import { z } from "zod";

export const UserSchema = z.object({
  id: z.number().int(),
  name: z.string().default("Jane Doe"),
});

export type User = z.infer<typeof UserSchema>;
