export type JwtTokens = {
  accessToken: string?;
  refreshToken: string?;
}

export type JwtTokenData = {
  userId: string?;
  email: string?;
}

export type User = {
  id: string?;
  email: string?;
  name: string?;
  role: string?;
}
