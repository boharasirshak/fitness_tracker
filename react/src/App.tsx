import { useSetAtom } from "jotai";
import { useEffect } from "react";
import { tokensAtom } from "./atom";
import { refreshJwtToken, verifyJwtToken } from "./lib/tokens";

import "./App.css";

function App() {
  const setTokens = useSetAtom(tokensAtom);

  useEffect(() => {
    async function checkJwt() {
      let accessToken = localStorage.getItem("access_token");
      let refreshToken = localStorage.getItem("refresh_token");

      if (!accessToken || !refreshToken) {
        return;
      }

      let isValid = await verifyJwtToken(accessToken);
      console.log(`Access token is: ${isValid ? "valid" : "invalid"}`);

      if (isValid) {
        setTokens({ accessToken, refreshToken });
        window.location.href = "/dashboard";
      } else {
        let { access_token, refresh_token } = await refreshJwtToken(
          refreshToken
        );

        if (access_token && refresh_token) {
          localStorage.setItem("access_token", access_token);
          localStorage.setItem("refresh_token", refresh_token);
          setTokens({ accessToken, refreshToken });
          window.location.href = "/dashboard";
        } else {
          console.log("Invalid refresh token. Goto login page.");
        }
      }
    }

    checkJwt();
    window.location.href = "/login";
  });

  return <></>;
}

export default App;
