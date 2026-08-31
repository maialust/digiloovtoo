import { Translation } from "./definition"

export default {
  propertyDefaults: {
    title: "Pealkirjata",
    description: "Kirjeldus puudub",
  },
  components: {
    callout: {
      note: "Märkus",
      abstract: "Kokkuvõte",
      info: "Info",
      todo: "Teha",
      tip: "Nõuanne",
      success: "Korras",
      question: "Küsimus",
      warning: "Hoiatus",
      failure: "Ebaõnnestumine",
      danger: "Oht",
      bug: "Viga",
      example: "Näide",
      quote: "Tsitaat",
    },
    backlinks: {
      title: "Tagasilingid",
      noBacklinksFound: "Tagasilinke ei leitud",
    },
    themeToggle: {
      lightMode: "Hele režiim",
      darkMode: "Tume režiim",
    },
    readerMode: {
      title: "Lugemisrežiim",
    },
    explorer: {
      title: "Sisupuu",
    },
    footer: {
      createdWith: "Loodud tööriistaga",
    },
    graph: {
      title: "Seosevaade",
    },
    recentNotes: {
      title: "Viimased märkmed",
      seeRemainingMore: ({ remaining }) => `Vaata veel ${remaining} →`,
    },
    transcludes: {
      transcludeOf: ({ targetSlug }) => `Sisu lehelt ${targetSlug}`,
      linkToOriginal: "Link originaalile",
    },
    search: {
      title: "Otsi",
      searchBarPlaceholder: "Otsi midagi",
    },
    tableOfContents: {
      title: "Sellel lehel",
    },
    contentMeta: {
      readingTime: ({ minutes }) => `${minutes} min lugemist`,
    },
  },
  pages: {
    rss: {
      recentNotes: "Viimased märkmed",
      lastFewNotes: ({ count }) => `Viimased ${count} märkust`,
    },
    error: {
      title: "Ei leitud",
      notFound: "See leht on kas privaatne või seda ei ole olemas.",
      home: "Tagasi avalehele",
    },
    folderContent: {
      folder: "Kaust",
      itemsUnderFolder: ({ count }) =>
        count === 1 ? "1 kirje selles kaustas." : `${count} kirjet selles kaustas.`,
    },
    tagContent: {
      tag: "Silt",
      tagIndex: "Siltide register",
      itemsUnderTag: ({ count }) =>
        count === 1 ? "1 kirje selle sildiga." : `${count} kirjet selle sildiga.`,
      showingFirst: ({ count }) => `Näidatakse esimest ${count} silti.`,
      totalTags: ({ count }) => `Leiti kokku ${count} silti.`,
    },
  },
} as const satisfies Translation
