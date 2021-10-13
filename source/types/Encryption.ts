export enum EncryptionType {
  DECRYPTED = "decrypted",
  PRIVATE_AES_KEY = "privateAesKey",
  SYMMETRIC_KEY = "symmetricKey",
}

export enum EncryptionErrorStatus {
  MISSING_AES_KEY = "missingAesKey",
}
export type EncryptionExceptionStatus = EncryptionErrorStatus | null;

export type CryptoNumber = number;
export type SerializedCryptoNumber = string;
export type PossiblySerializedCryptoNumber =
  | CryptoNumber
  | SerializedCryptoNumber;

export interface AesModule {
  pbkdf2: (
    password: string,
    salt: string,
    cost: number,
    lengthInBits: number
  ) => Promise<string>;
  encrypt: (text: string, key: string, iv: string) => Promise<string>;
  decrypt: (ciphertext: string, key: string, iv: string) => Promise<string>;
  hmac256: (ciphertext: string, key: string) => Promise<string>;
  randomKey: (lengthInBytes: number) => Promise<string>;
  sha1: (text: string) => Promise<string>;
  sha256: (text: string) => Promise<string>;
  sha512: (text: string) => Promise<string>;
}

declare module "react-native" {
  interface NativeModulesStatic {
    Aes: AesModule;
  }
}

export interface EncryptionDetails {
  type: EncryptionType;
  symmetricKeyName?: string;
  primes?: {
    P: PossiblySerializedCryptoNumber;
    G: PossiblySerializedCryptoNumber;
  };
  publicKeys?: Record<string, PossiblySerializedCryptoNumber | null>;
}

export interface EncryptionExceptionInterface extends Error {
  status: EncryptionExceptionStatus;
}