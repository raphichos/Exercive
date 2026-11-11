/**
 * Prettier settings for the frontend.
 *
 * Only the options that differ from Prettier's defaults are listed, chosen to match the
 * style the code already uses. Everything else (semicolons, trailing commas, 2-space
 * indent) stays at the default so there is less to argue about.
 *
 * @type {import('prettier').Config}
 */
const config = {
  singleQuote: true,
  printWidth: 100,
};

export default config;
