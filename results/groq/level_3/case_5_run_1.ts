import { z } from "zod";

const Hobby = z.object({
  name: z.string(),
  info: z.string(),
});

const User = z.object({
  hobbies: z.array(Hobby),
});
