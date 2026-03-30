export { part01 } from "./part01";
export { part02 } from "./part02";
export { part03 } from "./part03";
export { part04 } from "./part04";
export { part05 } from "./part05";
export { part06 } from "./part06";
export { part07 } from "./part07";
export { part08 } from "./part08";
export { part09 } from "./part09";
export { part10 } from "./part10";
export { part11 } from "./part11";
export { part12 } from "./part12";
export { part13 } from "./part13";
export { part14 } from "./part14";

import { part01 } from "./part01";
import { part02 } from "./part02";
import { part03 } from "./part03";
import { part04 } from "./part04";
import { part05 } from "./part05";
import { part06 } from "./part06";
import { part07 } from "./part07";
import { part08 } from "./part08";
import { part09 } from "./part09";
import { part10 } from "./part10";
import { part11 } from "./part11";
import { part12 } from "./part12";
import { part13 } from "./part13";
import { part14 } from "./part14";
import type { PartData } from "../../types";

export const allParts: PartData[] = [
  part01, part02, part03, part04, part05, part06, part07,
  part08, part09, part10, part11, part12, part13, part14,
];

export const partsById: Record<string, PartData> = Object.fromEntries(
  allParts.map((p) => [p.id, p])
);
