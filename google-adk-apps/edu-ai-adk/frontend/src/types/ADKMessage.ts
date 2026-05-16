export interface ADKMessage {
  author: string;
  content: {
    role: "user" | "model";
    parts: {
      text?: string;
    }[];
  };
  timestamp: number;
  actions: {
    transferToAgent?: string;
    artifactDelta?: any;
    stateDelta?: any;
  };
}
