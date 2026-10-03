import { useEffect, useRef } from "react";

const OTP_LENGTH = 6;

export default function OtpInput({
  value = "",
  onChange,
  disabled = false,
  autoFocus = false,
  error = false,
}) {
  const inputRefs = useRef([]);

  const focusBox = (index) => {
    const safeIndex = Math.max(
      0,
      Math.min(index, OTP_LENGTH - 1)
    );

    inputRefs.current[safeIndex]?.focus();
    inputRefs.current[safeIndex]?.select();
  };

  const updateValue = (rawValue, startIndex = 0) => {
    const digits = String(rawValue || "").replace(
      /\D/g,
      ""
    );

    if (!digits) {
      const chars = value
        .padEnd(OTP_LENGTH, "")
        .split("");

      chars[startIndex] = "";

      onChange(
        chars.join("").slice(0, OTP_LENGTH)
      );

      return;
    }

    const chars = value
      .padEnd(OTP_LENGTH, "")
      .split("");

    digits
      .slice(0, OTP_LENGTH - startIndex)
      .split("")
      .forEach((digit, offset) => {
        chars[startIndex + offset] = digit;
      });

    const nextValue = chars
      .join("")
      .slice(0, OTP_LENGTH);

    onChange(nextValue);

    const nextIndex = Math.min(
      startIndex + digits.length,
      OTP_LENGTH - 1
    );

    requestAnimationFrame(() => {
      focusBox(nextIndex);
    });
  };

  useEffect(() => {
    if (autoFocus) {
      requestAnimationFrame(() => {
        focusBox(0);
      });
    }
  }, [autoFocus]);

  function handleChange(index, event) {
    updateValue(
      event.target.value,
      index
    );
  }

  function handleKeyDown(index, event) {
    if (event.key === "Backspace") {
      event.preventDefault();

      const chars = value
        .padEnd(OTP_LENGTH, "")
        .split("");

      if (chars[index]) {
        chars[index] = "";

        onChange(
          chars.join("").slice(0, OTP_LENGTH)
        );

        return;
      }

      if (index > 0) {
        chars[index - 1] = "";

        onChange(
          chars.join("").slice(0, OTP_LENGTH)
        );

        requestAnimationFrame(() => {
          focusBox(index - 1);
        });
      }

      return;
    }

    if (event.key === "ArrowLeft") {
      event.preventDefault();
      focusBox(index - 1);
      return;
    }

    if (event.key === "ArrowRight") {
      event.preventDefault();
      focusBox(index + 1);
      return;
    }

    if (event.key === "Delete") {
      event.preventDefault();

      const chars = value
        .padEnd(OTP_LENGTH, "")
        .split("");

      chars[index] = "";

      onChange(
        chars.join("").slice(0, OTP_LENGTH)
      );
    }
  }

  function handlePaste(event) {
    event.preventDefault();

    const pasted = event.clipboardData
      .getData("text")
      .replace(/\D/g, "")
      .slice(0, OTP_LENGTH);

    if (!pasted) {
      return;
    }

    onChange(pasted);

    requestAnimationFrame(() => {
      focusBox(
        Math.min(
          pasted.length,
          OTP_LENGTH - 1
        )
      );
    });
  }

  function handleFocus(event) {
    event.target.select();
  }

  return (
    <div
      className="otp-input-group"
      role="group"
      aria-label="6 digit verification code"
      style={{
        display: "flex",
        justifyContent: "center",
        gap: "clamp(6px, 2vw, 10px)",
        margin: "8px 0 4px",
      }}
    >
      {Array.from({
        length: OTP_LENGTH,
      }).map((_, index) => (
        <input
          key={index}
          ref={(element) => {
            inputRefs.current[index] = element;
          }}
          className={`otp-box${
            error ? " otp-box-error" : ""
          }`}
          value={value[index] || ""}
          onChange={(event) =>
            handleChange(index, event)
          }
          onKeyDown={(event) =>
            handleKeyDown(index, event)
          }
          onPaste={handlePaste}
          onFocus={handleFocus}
          inputMode="numeric"
          pattern="[0-9]*"
          maxLength={OTP_LENGTH}
          autoComplete={
            index === 0
              ? "one-time-code"
              : "off"
          }
          aria-label={`OTP digit ${index + 1}`}
          disabled={disabled}
          style={{
            width: "clamp(40px, 10vw, 50px)",
            height: "52px",
            padding: 0,
            textAlign: "center",
            fontSize: "22px",
            fontWeight: 800,
            borderRadius: "10px",
            border: `1px solid ${
              error
                ? "#EF4444"
                : "#1E2536"
            }`,
            background: "#0B1020",
            color: "#F1F5FB",
            outline: "none",
            caretColor: "#22D3EE",
            boxSizing: "border-box",
            transition:
              "border-color .15s, box-shadow .15s",
          }}
        />
      ))}
    </div>
  );
}