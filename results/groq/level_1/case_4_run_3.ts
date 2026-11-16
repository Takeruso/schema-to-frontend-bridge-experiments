import { z } from "zod";

export const UserSchema = z.object({
  username: z.string(),
  email: z.string().optional().nullable(),
  full_name: z.string().optional().nullable(),
  disabled: z.boolean().optional().nullable(),
});
