import CenteredFlow from "../../ux/layouts/CenteredFlow";
import UploadDropzone from "../../ux/components/upload/UploadDropzone";
import Button from "../../ux/components/common/Button";
import { colors } from "../../ux/tokens/colors";

export default function SubmitPage() {
  return (
    <CenteredFlow>
      <h1 style={{ color: colors.textPrimary }}>
        Submit Your Photos
      </h1>

      <p style={{ color: colors.textMuted, marginTop: 16 }}>
        Images are evaluated for identity consistency and suitability.
        Not all submissions proceed — by design.
      </p>

      <UploadDropzone />

      <div style={{ marginTop: 32 }}>
        <Button>Continue</Button>
      </div>
    </CenteredFlow>
  );
}
