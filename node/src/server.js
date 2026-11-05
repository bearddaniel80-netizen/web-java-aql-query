import express from "express";
import cors from "cors";
import { forwardFastapi, postFastapi } from "./middleware/forewardFastapi.js";
import { upload, upload_to_fastapi } from "./utils/fastapi.js";

const app = express();

app.use(express.json());
app.use(cors());

/*
 * ==================================================
 * Dynamic Routes
 * ==================================================
 */
app.get(
  "/api/system/fields/:source",
  forwardFastapi(
    (req) => `/api/system/fields/${encodeURIComponent(req.params.source)}`
  )
);
app.get(
  "/api/system/:source",
  forwardFastapi(
    (req) => `/api/system/${encodeURIComponent(req.params.source)}`
  )
);
app.get(
  "/api/query/results/:jobId",
  forwardFastapi(
    (req) => `/api/query/results/${encodeURIComponent(req.params.jobId)}`
  )
);
app.post(
  "/api/query/submit/:query",
  postFastapi(
    (req) => `/api/query/submit/${encodeURIComponent(req.params.query)}`
  )
);
/*
 * ==================================================
 * Static Routes
 * ==================================================
 */
app.get("/api/data",
  forwardFastapi("/api/data")
);
app.get("/api/index",
  forwardFastapi("/api/index")
);
app.get("/api/system/list",
  forwardFastapi("/api/system/list")
);


app.post("/api/uploads",   upload.single("file"),
  async (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({
          error: "No file uploaded",
        });
      }

      const result = await upload_to_fastapi(
        "/api/uploads",
        req.file,
        {
          description: req.body.description,
        }
      );

      res
        .status(result.status)
        .json(result.data);

    } catch (error) {
      console.error("Upload failed:", error);

      res.status(500).json({
        error: "Upload failed",
      });
    }
  }
);
app.listen(4000, "0.0.0.0", () => {
  console.log("Server listening on port 4000");
});