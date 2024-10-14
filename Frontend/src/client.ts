import { createThirdwebClient } from "thirdweb";

// Replace this with your client ID string
// refer to https://portal.thirdweb.com/typescript/v5/client on how to get a client ID
const clientId = import.meta.env.CLIENT_ID;

export const client = createThirdwebClient({
  clientId: '5e280fd31c81bd23ce26d726471b2506',
});
