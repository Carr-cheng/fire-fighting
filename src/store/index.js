import { createStore  } from "vuex";

import login from "./login"
import layout from "./layout";
import search_fire from "./search_fire";
import dispatch_mapPath from "./dispatch_mapPath";
import dispatch_car from "./dispatch_car";
import search_station from "./search_station"
export default  createStore ({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    layout: layout,
    search_fire: search_fire,
    dispatch_mapPath: dispatch_mapPath,
    dispatch_car: dispatch_car,
    search_station: search_station,
    login: login,
  },
});
