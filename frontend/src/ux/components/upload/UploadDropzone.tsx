import { colors } from "../../tokens/colors";

export default function UploadDropzone() {
  return (
    <div
      style={{
        border: "1px dashed #2A2F3A",
        borderRadius: 4,
        padding: 48,
        textAlign: "center",
        color: colors.textMuted,
        marginTop: 32,
      }}
    >
      Drag images here<br />
      or click to browse
    </div>
  );
}
