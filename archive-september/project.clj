(defproject sence "0.1.0"
  :description 
  "sence is complicated"
  :url "github.com/LSaldyt/sence"
  :license {:name "Eclipse Public License"}
  :dependencies [[org.clojure/clojure "1.8.0"]
                 [org.clojure/tools.cli "0.2.4"]
                 [org.clojure/math.numeric-tower "0.0.4"]
                 [ari "0.1.0"]
                 [paradex "0.1.0"]]
  :plugins [[lein-bin "0.3.4"]
            [lein-marginalia "0.9.1"]]
  :bin { :name "ari" }
  :main sence.core)
