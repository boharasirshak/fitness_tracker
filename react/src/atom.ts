import { atom } from "jotai";
import { JwtTokenData, JwtTokens, User } from "./types";

export const tokensAtom = atom<JwtTokens>({
  accessToken: null,
  refreshToken: null
});

export const tokenDataAtom = atom<JwtTokenData>({
  userId: null,
  email: null
});

export const userAtom = atom<User>({
  id: null,
  email: null,
  name: null,
  role: null
});
