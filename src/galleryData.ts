export type GalleryItem = {
  title: string;
  caption: string;
  imageSrc?: string;
  imageAlt?: string;
};

export const galleryItems: readonly GalleryItem[] = [
  {
    title: "VR + PC energy",
    caption:
      "A quick look at the immersive and PC side of inFAMOUS — neon lighting, focused stations, and a strong gaming atmosphere.",
    imageSrc: "./gallery-vr-pc.png",
    imageAlt: "VR play and PC gaming setup inside inFAMOUS Gaming Cafe",
  },
  {
    title: "Console lounge",
    caption:
      "PlayStation sessions feel easy and social, whether it is a head-to-head match or a relaxed couch session with friends.",
    imageSrc: "./gallery-console-lounge.png",
    imageAlt: "Friends playing console games in the PlayStation lounge at inFAMOUS Gaming Cafe",
  },
  {
    title: "Billiards + table tennis",
    caption:
      "Not every session has to stay on-screen — pool, snooker, and table tennis add a strong off-screen competition vibe.",
    imageSrc: "./gallery-billiards-tt.png",
    imageAlt: "Billiards tables and table tennis setup inside inFAMOUS Gaming Cafe",
  },
  {
    title: "Events & community",
    caption:
      "The space also works well for events, gaming communities, and brand-led activations that bring the crowd together.",
    imageSrc: "./gallery-events.png",
    imageAlt: "Community event photos inside inFAMOUS Gaming Cafe",
  },
] as const;
