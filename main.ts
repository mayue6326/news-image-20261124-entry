// Entry program for the news-image-20261124 bounty.
// It ships one finished picture: entry.png sits next to this file in the
// repository, and the program validates that picture, then copies it
// byte-for-byte to the output folder the grader expects.
// Only Node's standard library is used. No network, no randomness,
// no clocks — the same input always produces the same output bytes.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1024 * 1024; // 1 MiB
const MAX_EDGE = 1024; // pixels per side

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(targetDir, "entry.png");

if (!existsSync(source)) {
  throw new Error(`missing input image: ${source}`);
}

const size = statSync(source).size;
if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}

// PNG layout: 8-byte signature, then the IHDR chunk whose data starts
// with width and height as big-endian 32-bit integers at bytes 16..24.
// A JPEG (magic bytes FF D8 FF) is also a legal entry format, so the
// format is sniffed first and JPEG dimensions are read from its SOF0
// marker (FF C0) instead of the PNG header.
const bytes = readFileSync(source);
const signature = [137, 80, 78, 71, 13, 10, 26, 10];
const looksLikePng = signature.every((byte, index) => bytes[index] === byte);
const looksLikeJpeg = bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff;
let width = 0;
let height = 0;
let format = "";
if (looksLikePng) {
  format = "PNG";
  width = bytes.readUInt32BE(16);
  height = bytes.readUInt32BE(20);
} else if (looksLikeJpeg) {
  format = "JPEG";
  for (let i = 2; i + 9 < bytes.length; i += 1) {
    if (bytes[i] === 0xff && bytes[i + 1] === 0xc0) {
      height = bytes.readUInt16BE(i + 5);
      width = bytes.readUInt16BE(i + 7);
      break;
    }
  }
  if (width === 0 || height === 0) {
    throw new Error("could not read JPEG dimensions from a SOF0 marker");
  }
} else {
  throw new Error("entry.png is neither PNG nor JPEG by magic bytes");
}
if (width > MAX_EDGE || height > MAX_EDGE) {
  throw new Error(`entry.png is ${width}x${height}, over the ${MAX_EDGE}x${MAX_EDGE} limit`);
}

mkdirSync(targetDir, { recursive: true });
copyFileSync(source, target);

console.log(`entry.png [${format}] ${width}x${height} ${size} bytes -> ${target}`);
