export { pg01 } from "./pg01";
export { pg02 } from "./pg02";
export { pg03 } from "./pg03";
export { pg04 } from "./pg04";
export { pg05 } from "./pg05";
export { pg06 } from "./pg06";
export { pg07 } from "./pg07";
export { pg08 } from "./pg08";
export { pg09 } from "./pg09";
export { pg10 } from "./pg10";
export { pg11 } from "./pg11";
export { pg12 } from "./pg12";
export { pg13 } from "./pg13";
export { pg14 } from "./pg14";

import { pg01 } from "./pg01";
import { pg02 } from "./pg02";
import { pg03 } from "./pg03";
import { pg04 } from "./pg04";
import { pg05 } from "./pg05";
import { pg06 } from "./pg06";
import { pg07 } from "./pg07";
import { pg08 } from "./pg08";
import { pg09 } from "./pg09";
import { pg10 } from "./pg10";
import { pg11 } from "./pg11";
import { pg12 } from "./pg12";
import { pg13 } from "./pg13";
import { pg14 } from "./pg14";
import type { PlaygroundConfig } from "../../types";

export const allPlaygrounds: PlaygroundConfig[] = [
  pg01, pg02, pg03, pg04, pg05, pg06, pg07,
  pg08, pg09, pg10, pg11, pg12, pg13, pg14,
];

export const playgroundById: Record<string, PlaygroundConfig> = Object.fromEntries(
  allPlaygrounds.map((pg) => [pg.partId, pg])
);
