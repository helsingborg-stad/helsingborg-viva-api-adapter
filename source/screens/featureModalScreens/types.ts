import { RouteProp } from "@react-navigation/native";
import { StackNavigationProp } from "@react-navigation/stack";

export enum ModalScreen {
  "Features",
  "ServiceSelections",
  "Help",
}

export type ModalScreenType = {
  component: React.FC<any>;
  title: string;
  propagateSwipe?: boolean;
  colorSchema?: string;
};

export type FeatureModalScreenProp = RouteProp<any, "FeatureModal">;
export type FeatureModalNavigationProp = StackNavigationProp<
  any,
  "FeatureModal"
>;
