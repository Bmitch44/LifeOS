export function assertNever(x: never): never {
  throw new Error(`Unexpected object: ${x}`)
}

export function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}


