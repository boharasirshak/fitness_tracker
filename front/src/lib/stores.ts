import { writable } from "svelte/store";
import type { JwtTokenData, User } from "./type";

export const accessToken = writable<string | null>(null);
export const refreshToken = writable<string | null>(null);
export const user = writable<User | null>(null);
export const tokenData = writable<JwtTokenData>();
export const isAuthenticated = writable<boolean>(false);
