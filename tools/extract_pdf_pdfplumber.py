"""
PDFファイルからテキストを抽出するツール（pdfplumber優先版）
"""
import sys
from pathlib import Path


def extract_text_from_pdf_with_pdfplumber(pdf_path: str, output_path: str):
    """pdfplumberを使用してPDFからテキストを抽出"""
    import pdfplumber
    
    with pdfplumber.open(pdf_path) as pdf:
        text = []
        
        print(f"総ページ数: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages):
            print(f"ページ {i+1}/{len(pdf.pages)} を処理中...")
            page_text = page.extract_text()
            if page_text:
                text.append(
                    f"\n{'='*60}\n"
                    f"ページ {i+1}\n"
                    f"{'='*60}\n"
                    f"{page_text}"
                )
        
        full_text = '\n'.join(text)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as out_file:
                out_file.write(full_text)
            print(f"\n✅ テキストを {output_path} に保存しました")
        
        return full_text


def main():
    if len(sys.argv) < 2:
        print(
            "使用方法: python extract_pdf_pdfplumber.py "
            "<PDFファイルパス> [出力先テキストファイルパス]"
        )
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(pdf_path).exists():
        print(f"❌ エラー: ファイルが見つかりません: {pdf_path}")
        sys.exit(1)
    
    # 出力パスが指定されていない場合、デフォルトのパスを生成
    if not output_path:
        pdf_file = Path(pdf_path)
        output_path = str(
            pdf_file.parent / f"{pdf_file.stem}_pdfplumber.txt"
        )
    
    print(f"\n📄 PDFファイル: {pdf_path}")
    print(f"📝 出力先: {output_path}\n")
    
    try:
        text = extract_text_from_pdf_with_pdfplumber(pdf_path, output_path)
        
        if text:
            print(f"\n✅ 完了！抽出された文字数: {len(text)}")
            print(f"\n最初の1000文字のプレビュー:")
            print("-" * 60)
            print(text[:1000])
            print("-" * 60)
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
