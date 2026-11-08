// macOS Vision で画像を OCR する(日本語)。手元だけで動き、画像を外へ送らない。
// 使い方: swift src/ocr_vision.swift page.png > page.txt
import Foundation
import Vision
import AppKit

let path = CommandLine.arguments[1]
guard let img = NSImage(contentsOfFile: path),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    fputs("cannot read \(path)\n", stderr); exit(1)
}
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.recognitionLanguages = ["ja-JP"]
req.usesLanguageCorrection = true
try VNImageRequestHandler(cgImage: cg).perform([req])
// 上から下、左から右の順に並べる(Vision の座標は左下が原点)
let obs = (req.results ?? []).sorted {
    abs($0.boundingBox.midY - $1.boundingBox.midY) > 0.01 ? $0.boundingBox.midY > $1.boundingBox.midY
                                                         : $0.boundingBox.minX < $1.boundingBox.minX
}
for o in obs { if let t = o.topCandidates(1).first { print(t.string) } }
