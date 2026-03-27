// types.ts

export type CoreEngineError =
  | {
      code: 'ERROR_CODE';
      message: string;
      details?: any;
    }
  | {
      code: 'UNKNOWN_ERROR';
      message: string;
      details?: any;
    };

export type CoreEngineConfig = {
  debug: boolean;
};

export type CoreEngineOptions = {
  config: CoreEngineConfig;
};

export type CoreEngineResult<T> =
  | {
      type: 'result';
      value: T;
      error?: never;
    }
  | {
      type: 'error';
      error: CoreEngineError;
      value?: never;
    };