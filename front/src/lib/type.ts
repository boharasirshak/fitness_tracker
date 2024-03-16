export type JwtTokenData = {
  userId: string | undefined;
  email: string | undefined;
}

export type User = {
  id: string | undefined;
  email: string | undefined;
  name: string | undefined;
  role: string | undefined;
}

export type Error = {
  statusText: string;
  message: string;
}

export enum AlertType {
  Success = "success",
  Error = "error",
  // Warning = "warning",
  // Info = "info",
}
