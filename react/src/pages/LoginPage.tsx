import { useSetAtom } from "jotai";
import { useEffect, useState } from "react";
import { tokensAtom } from "../atom";
import { refreshJwtToken, verifyJwtToken } from "../lib/tokens";

import FailureAlert from "../components/alerts/FailureAlert";
import SuccessAlert from "../components/alerts/SuccessAlert";

const LoginPage = () => {
  const setTokens = useSetAtom(tokensAtom);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);
  const [isFailure, setIsFailure] = useState(false);
  const [message, setMessage] = useState("");

  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

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
  });

  function showPopup(success: boolean, msg: string) {
    if (success) {
      setIsSuccess(true);
      setIsFailure(false);
      setMessage(msg);
    } else {
      setIsSuccess(false);
      setIsFailure(true);
      setMessage(msg);
    }
  }

  async function login() {
    let response = await fetch(`${BACKEND_URL}/api/v1/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    let data = await response.json();
    if (response.status === 401) {
      showPopup(false, data.detail);

    } else if (response.status === 422) {
      showPopup(false, data.detail[0].msg);

    } else if (data.access_token && data.refresh_token) {
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      setTokens({
        accessToken: data.access_token,
        refreshToken: data.refresh_token,
      });
      showPopup(true, "Login successful");
      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 1000);
      
    } else {
      showPopup(false, "Unknown error");
    }
  }

  return (
    <>
      <section className="bg-gray-50 dark:bg-gray-900">
        <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
          <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
            <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
              <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                Sign in to your account
              </h1>
              <div className="space-y-4 md:space-y-6">
                <div>
                  <label
                    htmlFor="email"
                    className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                  >
                    Your email
                  </label>
                  <input
                    type="email"
                    name="email"
                    id="email"
                    className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="name@company.com"
                    onInput={(e) => {
                      setEmail(e.currentTarget.value);
                    }}
                  />
                </div>
                <div>
                  <label
                    htmlFor="password"
                    className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                  >
                    Password
                  </label>
                  <input
                    type="password"
                    name="password"
                    id="password"
                    placeholder="••••••••"
                    className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    onInput={(e) => {
                      setPassword(e.currentTarget.value);
                    }}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-start">
                    <div className="flex items-center h-5">
                      <input
                        id="remember"
                        aria-describedby="remember"
                        type="checkbox"
                        className="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800"
                        required
                      />
                    </div>
                    <div className="ml-3 text-sm">
                      <label
                        htmlFor="remember"
                        className="text-gray-500 dark:text-gray-300"
                      >
                        Remember me
                      </label>
                    </div>
                  </div>
                  {/* Forget password not implemented now */}
                  {/* <a href="#" className="text-sm font-medium text-primary-600 hover:underline dark:text-primary-500">htmlForgot password?</a> */}
                </div>
                <button
                  type="submit"
                  id="submit"
                  className="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
                  onClick={login}
                >
                  Sign in
                </button>
                <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                  Don’t have an account yet?{" "}
                  <a
                    href="/register"
                    className="font-medium text-primary-600 hover:underline dark:text-primary-500"
                  >
                    Register Now
                  </a>
                </p>
              </div>
            </div>
          </div>
        </div>
        <SuccessAlert message={message} visible={isSuccess} />
        <FailureAlert message={message} visible={isFailure} />
      </section>
    </>
  );
};

export default LoginPage;
