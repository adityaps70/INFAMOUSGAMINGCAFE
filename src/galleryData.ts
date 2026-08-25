export type GalleryItem = {
  title: string;
  caption: string;
  imageSrc?: string;
  imageAlt?: string;
};

export const galleryItems: readonly GalleryItem[] = [
  {
    title: "The arena",
    caption: "Start with the main arena energy: focused sessions, quick drop-ins, and longer crew plans.",
  },
  {
    title: "Controller time",
    caption: "Controller-led sessions for head-to-head rivalry, shared play, and easy group time.",
  },
  {
    title: "Beyond the screen",
    caption: "Switch the pace with immersive, steering, and simulator-style experiences.",
  },
  {
    title: "Crew mode",
    caption: "Bring friends, plan a celebration, or make the gaming session the hangout.",
  },
] as const;
