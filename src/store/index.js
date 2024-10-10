import { createStore  } from "vuex";

import layout from "./layout";
import search_fire from "./search_fire";
import rank_live from "./rank_live";
import rank_gift from "./rank_gift";
import search_station from "./search_station"

export default  createStore ({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    layout: layout,
    search_fire: search_fire,
    rank_live: rank_live,
    rank_gift: rank_gift,
    search_station: search_station,

  },
});
