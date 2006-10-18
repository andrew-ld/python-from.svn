#include "pgenheaders.h"
#include "grammar.h"
static arc arcs_0_0[3] = {
	{2, 1},
	{3, 1},
	{4, 2},
};
static arc arcs_0_1[1] = {
	{0, 1},
};
static arc arcs_0_2[1] = {
	{2, 1},
};
static state states_0[3] = {
	{3, arcs_0_0},
	{1, arcs_0_1},
	{1, arcs_0_2},
};
static arc arcs_1_0[3] = {
	{2, 0},
	{6, 0},
	{7, 1},
};
static arc arcs_1_1[1] = {
	{0, 1},
};
static state states_1[2] = {
	{3, arcs_1_0},
	{1, arcs_1_1},
};
static arc arcs_2_0[1] = {
	{9, 1},
};
static arc arcs_2_1[2] = {
	{2, 1},
	{7, 2},
};
static arc arcs_2_2[1] = {
	{0, 2},
};
static state states_2[3] = {
	{1, arcs_2_0},
	{2, arcs_2_1},
	{1, arcs_2_2},
};
static arc arcs_3_0[1] = {
	{11, 1},
};
static arc arcs_3_1[1] = {
	{12, 2},
};
static arc arcs_3_2[2] = {
	{13, 3},
	{2, 4},
};
static arc arcs_3_3[2] = {
	{14, 5},
	{15, 6},
};
static arc arcs_3_4[1] = {
	{0, 4},
};
static arc arcs_3_5[1] = {
	{15, 6},
};
static arc arcs_3_6[1] = {
	{2, 4},
};
static state states_3[7] = {
	{1, arcs_3_0},
	{1, arcs_3_1},
	{2, arcs_3_2},
	{2, arcs_3_3},
	{1, arcs_3_4},
	{1, arcs_3_5},
	{1, arcs_3_6},
};
static arc arcs_4_0[1] = {
	{10, 1},
};
static arc arcs_4_1[2] = {
	{10, 1},
	{0, 1},
};
static state states_4[2] = {
	{1, arcs_4_0},
	{2, arcs_4_1},
};
static arc arcs_5_0[2] = {
	{16, 1},
	{18, 2},
};
static arc arcs_5_1[1] = {
	{18, 2},
};
static arc arcs_5_2[1] = {
	{19, 3},
};
static arc arcs_5_3[1] = {
	{20, 4},
};
static arc arcs_5_4[1] = {
	{21, 5},
};
static arc arcs_5_5[1] = {
	{22, 6},
};
static arc arcs_5_6[1] = {
	{0, 6},
};
static state states_5[7] = {
	{2, arcs_5_0},
	{1, arcs_5_1},
	{1, arcs_5_2},
	{1, arcs_5_3},
	{1, arcs_5_4},
	{1, arcs_5_5},
	{1, arcs_5_6},
};
static arc arcs_6_0[1] = {
	{13, 1},
};
static arc arcs_6_1[2] = {
	{23, 2},
	{15, 3},
};
static arc arcs_6_2[1] = {
	{15, 3},
};
static arc arcs_6_3[1] = {
	{0, 3},
};
static state states_6[4] = {
	{1, arcs_6_0},
	{2, arcs_6_1},
	{1, arcs_6_2},
	{1, arcs_6_3},
};
static arc arcs_7_0[3] = {
	{24, 1},
	{28, 2},
	{29, 3},
};
static arc arcs_7_1[3] = {
	{25, 4},
	{27, 5},
	{0, 1},
};
static arc arcs_7_2[1] = {
	{19, 6},
};
static arc arcs_7_3[1] = {
	{19, 7},
};
static arc arcs_7_4[1] = {
	{26, 8},
};
static arc arcs_7_5[4] = {
	{24, 1},
	{28, 2},
	{29, 3},
	{0, 5},
};
static arc arcs_7_6[2] = {
	{27, 9},
	{0, 6},
};
static arc arcs_7_7[1] = {
	{0, 7},
};
static arc arcs_7_8[2] = {
	{27, 5},
	{0, 8},
};
static arc arcs_7_9[1] = {
	{29, 3},
};
static state states_7[10] = {
	{3, arcs_7_0},
	{3, arcs_7_1},
	{1, arcs_7_2},
	{1, arcs_7_3},
	{1, arcs_7_4},
	{4, arcs_7_5},
	{2, arcs_7_6},
	{1, arcs_7_7},
	{2, arcs_7_8},
	{1, arcs_7_9},
};
static arc arcs_8_0[2] = {
	{19, 1},
	{13, 2},
};
static arc arcs_8_1[1] = {
	{0, 1},
};
static arc arcs_8_2[1] = {
	{30, 3},
};
static arc arcs_8_3[1] = {
	{15, 1},
};
static state states_8[4] = {
	{2, arcs_8_0},
	{1, arcs_8_1},
	{1, arcs_8_2},
	{1, arcs_8_3},
};
static arc arcs_9_0[1] = {
	{24, 1},
};
static arc arcs_9_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_9_2[2] = {
	{24, 1},
	{0, 2},
};
static state states_9[3] = {
	{1, arcs_9_0},
	{2, arcs_9_1},
	{2, arcs_9_2},
};
static arc arcs_10_0[2] = {
	{3, 1},
	{4, 1},
};
static arc arcs_10_1[1] = {
	{0, 1},
};
static state states_10[2] = {
	{2, arcs_10_0},
	{1, arcs_10_1},
};
static arc arcs_11_0[1] = {
	{31, 1},
};
static arc arcs_11_1[2] = {
	{32, 2},
	{2, 3},
};
static arc arcs_11_2[2] = {
	{31, 1},
	{2, 3},
};
static arc arcs_11_3[1] = {
	{0, 3},
};
static state states_11[4] = {
	{1, arcs_11_0},
	{2, arcs_11_1},
	{2, arcs_11_2},
	{1, arcs_11_3},
};
static arc arcs_12_0[9] = {
	{33, 1},
	{34, 1},
	{35, 1},
	{36, 1},
	{37, 1},
	{38, 1},
	{39, 1},
	{40, 1},
	{41, 1},
};
static arc arcs_12_1[1] = {
	{0, 1},
};
static state states_12[2] = {
	{9, arcs_12_0},
	{1, arcs_12_1},
};
static arc arcs_13_0[1] = {
	{9, 1},
};
static arc arcs_13_1[3] = {
	{42, 2},
	{25, 3},
	{0, 1},
};
static arc arcs_13_2[1] = {
	{9, 4},
};
static arc arcs_13_3[1] = {
	{9, 5},
};
static arc arcs_13_4[1] = {
	{0, 4},
};
static arc arcs_13_5[2] = {
	{25, 3},
	{0, 5},
};
static state states_13[6] = {
	{1, arcs_13_0},
	{3, arcs_13_1},
	{1, arcs_13_2},
	{1, arcs_13_3},
	{1, arcs_13_4},
	{2, arcs_13_5},
};
static arc arcs_14_0[12] = {
	{43, 1},
	{44, 1},
	{45, 1},
	{46, 1},
	{47, 1},
	{48, 1},
	{49, 1},
	{50, 1},
	{51, 1},
	{52, 1},
	{53, 1},
	{54, 1},
};
static arc arcs_14_1[1] = {
	{0, 1},
};
static state states_14[2] = {
	{12, arcs_14_0},
	{1, arcs_14_1},
};
static arc arcs_15_0[1] = {
	{55, 1},
};
static arc arcs_15_1[3] = {
	{26, 2},
	{56, 3},
	{0, 1},
};
static arc arcs_15_2[2] = {
	{27, 4},
	{0, 2},
};
static arc arcs_15_3[1] = {
	{26, 5},
};
static arc arcs_15_4[2] = {
	{26, 2},
	{0, 4},
};
static arc arcs_15_5[2] = {
	{27, 6},
	{0, 5},
};
static arc arcs_15_6[1] = {
	{26, 7},
};
static arc arcs_15_7[2] = {
	{27, 8},
	{0, 7},
};
static arc arcs_15_8[2] = {
	{26, 7},
	{0, 8},
};
static state states_15[9] = {
	{1, arcs_15_0},
	{3, arcs_15_1},
	{2, arcs_15_2},
	{1, arcs_15_3},
	{2, arcs_15_4},
	{2, arcs_15_5},
	{1, arcs_15_6},
	{2, arcs_15_7},
	{2, arcs_15_8},
};
static arc arcs_16_0[1] = {
	{57, 1},
};
static arc arcs_16_1[1] = {
	{58, 2},
};
static arc arcs_16_2[1] = {
	{0, 2},
};
static state states_16[3] = {
	{1, arcs_16_0},
	{1, arcs_16_1},
	{1, arcs_16_2},
};
static arc arcs_17_0[1] = {
	{59, 1},
};
static arc arcs_17_1[1] = {
	{0, 1},
};
static state states_17[2] = {
	{1, arcs_17_0},
	{1, arcs_17_1},
};
static arc arcs_18_0[5] = {
	{60, 1},
	{61, 1},
	{62, 1},
	{63, 1},
	{64, 1},
};
static arc arcs_18_1[1] = {
	{0, 1},
};
static state states_18[2] = {
	{5, arcs_18_0},
	{1, arcs_18_1},
};
static arc arcs_19_0[1] = {
	{65, 1},
};
static arc arcs_19_1[1] = {
	{0, 1},
};
static state states_19[2] = {
	{1, arcs_19_0},
	{1, arcs_19_1},
};
static arc arcs_20_0[1] = {
	{66, 1},
};
static arc arcs_20_1[1] = {
	{0, 1},
};
static state states_20[2] = {
	{1, arcs_20_0},
	{1, arcs_20_1},
};
static arc arcs_21_0[1] = {
	{67, 1},
};
static arc arcs_21_1[2] = {
	{9, 2},
	{0, 1},
};
static arc arcs_21_2[1] = {
	{0, 2},
};
static state states_21[3] = {
	{1, arcs_21_0},
	{2, arcs_21_1},
	{1, arcs_21_2},
};
static arc arcs_22_0[1] = {
	{68, 1},
};
static arc arcs_22_1[1] = {
	{9, 2},
};
static arc arcs_22_2[1] = {
	{0, 2},
};
static state states_22[3] = {
	{1, arcs_22_0},
	{1, arcs_22_1},
	{1, arcs_22_2},
};
static arc arcs_23_0[1] = {
	{69, 1},
};
static arc arcs_23_1[2] = {
	{26, 2},
	{0, 1},
};
static arc arcs_23_2[2] = {
	{27, 3},
	{0, 2},
};
static arc arcs_23_3[1] = {
	{26, 4},
};
static arc arcs_23_4[2] = {
	{27, 5},
	{0, 4},
};
static arc arcs_23_5[1] = {
	{26, 6},
};
static arc arcs_23_6[1] = {
	{0, 6},
};
static state states_23[7] = {
	{1, arcs_23_0},
	{2, arcs_23_1},
	{2, arcs_23_2},
	{1, arcs_23_3},
	{2, arcs_23_4},
	{1, arcs_23_5},
	{1, arcs_23_6},
};
static arc arcs_24_0[2] = {
	{70, 1},
	{71, 1},
};
static arc arcs_24_1[1] = {
	{0, 1},
};
static state states_24[2] = {
	{2, arcs_24_0},
	{1, arcs_24_1},
};
static arc arcs_25_0[1] = {
	{72, 1},
};
static arc arcs_25_1[1] = {
	{73, 2},
};
static arc arcs_25_2[1] = {
	{0, 2},
};
static state states_25[3] = {
	{1, arcs_25_0},
	{1, arcs_25_1},
	{1, arcs_25_2},
};
static arc arcs_26_0[1] = {
	{74, 1},
};
static arc arcs_26_1[1] = {
	{12, 2},
};
static arc arcs_26_2[1] = {
	{72, 3},
};
static arc arcs_26_3[3] = {
	{28, 4},
	{13, 5},
	{75, 4},
};
static arc arcs_26_4[1] = {
	{0, 4},
};
static arc arcs_26_5[1] = {
	{75, 6},
};
static arc arcs_26_6[1] = {
	{15, 4},
};
static state states_26[7] = {
	{1, arcs_26_0},
	{1, arcs_26_1},
	{1, arcs_26_2},
	{3, arcs_26_3},
	{1, arcs_26_4},
	{1, arcs_26_5},
	{1, arcs_26_6},
};
static arc arcs_27_0[1] = {
	{19, 1},
};
static arc arcs_27_1[2] = {
	{19, 2},
	{0, 1},
};
static arc arcs_27_2[1] = {
	{19, 3},
};
static arc arcs_27_3[1] = {
	{0, 3},
};
static state states_27[4] = {
	{1, arcs_27_0},
	{2, arcs_27_1},
	{1, arcs_27_2},
	{1, arcs_27_3},
};
static arc arcs_28_0[1] = {
	{12, 1},
};
static arc arcs_28_1[2] = {
	{19, 2},
	{0, 1},
};
static arc arcs_28_2[1] = {
	{19, 3},
};
static arc arcs_28_3[1] = {
	{0, 3},
};
static state states_28[4] = {
	{1, arcs_28_0},
	{2, arcs_28_1},
	{1, arcs_28_2},
	{1, arcs_28_3},
};
static arc arcs_29_0[1] = {
	{76, 1},
};
static arc arcs_29_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_29_2[2] = {
	{76, 1},
	{0, 2},
};
static state states_29[3] = {
	{1, arcs_29_0},
	{2, arcs_29_1},
	{2, arcs_29_2},
};
static arc arcs_30_0[1] = {
	{77, 1},
};
static arc arcs_30_1[2] = {
	{27, 0},
	{0, 1},
};
static state states_30[2] = {
	{1, arcs_30_0},
	{2, arcs_30_1},
};
static arc arcs_31_0[1] = {
	{19, 1},
};
static arc arcs_31_1[2] = {
	{78, 0},
	{0, 1},
};
static state states_31[2] = {
	{1, arcs_31_0},
	{2, arcs_31_1},
};
static arc arcs_32_0[1] = {
	{79, 1},
};
static arc arcs_32_1[1] = {
	{19, 2},
};
static arc arcs_32_2[2] = {
	{27, 1},
	{0, 2},
};
static state states_32[3] = {
	{1, arcs_32_0},
	{1, arcs_32_1},
	{2, arcs_32_2},
};
static arc arcs_33_0[1] = {
	{80, 1},
};
static arc arcs_33_1[1] = {
	{81, 2},
};
static arc arcs_33_2[2] = {
	{82, 3},
	{0, 2},
};
static arc arcs_33_3[1] = {
	{26, 4},
};
static arc arcs_33_4[2] = {
	{27, 5},
	{0, 4},
};
static arc arcs_33_5[1] = {
	{26, 6},
};
static arc arcs_33_6[1] = {
	{0, 6},
};
static state states_33[7] = {
	{1, arcs_33_0},
	{1, arcs_33_1},
	{2, arcs_33_2},
	{1, arcs_33_3},
	{2, arcs_33_4},
	{1, arcs_33_5},
	{1, arcs_33_6},
};
static arc arcs_34_0[1] = {
	{83, 1},
};
static arc arcs_34_1[1] = {
	{26, 2},
};
static arc arcs_34_2[2] = {
	{27, 3},
	{0, 2},
};
static arc arcs_34_3[1] = {
	{26, 4},
};
static arc arcs_34_4[1] = {
	{0, 4},
};
static state states_34[5] = {
	{1, arcs_34_0},
	{1, arcs_34_1},
	{2, arcs_34_2},
	{1, arcs_34_3},
	{1, arcs_34_4},
};
static arc arcs_35_0[6] = {
	{84, 1},
	{85, 1},
	{86, 1},
	{87, 1},
	{17, 1},
	{88, 1},
};
static arc arcs_35_1[1] = {
	{0, 1},
};
static state states_35[2] = {
	{6, arcs_35_0},
	{1, arcs_35_1},
};
static arc arcs_36_0[1] = {
	{89, 1},
};
static arc arcs_36_1[1] = {
	{26, 2},
};
static arc arcs_36_2[1] = {
	{21, 3},
};
static arc arcs_36_3[1] = {
	{22, 4},
};
static arc arcs_36_4[3] = {
	{90, 1},
	{91, 5},
	{0, 4},
};
static arc arcs_36_5[1] = {
	{21, 6},
};
static arc arcs_36_6[1] = {
	{22, 7},
};
static arc arcs_36_7[1] = {
	{0, 7},
};
static state states_36[8] = {
	{1, arcs_36_0},
	{1, arcs_36_1},
	{1, arcs_36_2},
	{1, arcs_36_3},
	{3, arcs_36_4},
	{1, arcs_36_5},
	{1, arcs_36_6},
	{1, arcs_36_7},
};
static arc arcs_37_0[1] = {
	{92, 1},
};
static arc arcs_37_1[1] = {
	{26, 2},
};
static arc arcs_37_2[1] = {
	{21, 3},
};
static arc arcs_37_3[1] = {
	{22, 4},
};
static arc arcs_37_4[2] = {
	{91, 5},
	{0, 4},
};
static arc arcs_37_5[1] = {
	{21, 6},
};
static arc arcs_37_6[1] = {
	{22, 7},
};
static arc arcs_37_7[1] = {
	{0, 7},
};
static state states_37[8] = {
	{1, arcs_37_0},
	{1, arcs_37_1},
	{1, arcs_37_2},
	{1, arcs_37_3},
	{2, arcs_37_4},
	{1, arcs_37_5},
	{1, arcs_37_6},
	{1, arcs_37_7},
};
static arc arcs_38_0[1] = {
	{93, 1},
};
static arc arcs_38_1[1] = {
	{58, 2},
};
static arc arcs_38_2[1] = {
	{82, 3},
};
static arc arcs_38_3[1] = {
	{9, 4},
};
static arc arcs_38_4[1] = {
	{21, 5},
};
static arc arcs_38_5[1] = {
	{22, 6},
};
static arc arcs_38_6[2] = {
	{91, 7},
	{0, 6},
};
static arc arcs_38_7[1] = {
	{21, 8},
};
static arc arcs_38_8[1] = {
	{22, 9},
};
static arc arcs_38_9[1] = {
	{0, 9},
};
static state states_38[10] = {
	{1, arcs_38_0},
	{1, arcs_38_1},
	{1, arcs_38_2},
	{1, arcs_38_3},
	{1, arcs_38_4},
	{1, arcs_38_5},
	{2, arcs_38_6},
	{1, arcs_38_7},
	{1, arcs_38_8},
	{1, arcs_38_9},
};
static arc arcs_39_0[1] = {
	{94, 1},
};
static arc arcs_39_1[1] = {
	{21, 2},
};
static arc arcs_39_2[1] = {
	{22, 3},
};
static arc arcs_39_3[2] = {
	{95, 4},
	{96, 5},
};
static arc arcs_39_4[1] = {
	{21, 6},
};
static arc arcs_39_5[1] = {
	{21, 7},
};
static arc arcs_39_6[1] = {
	{22, 8},
};
static arc arcs_39_7[1] = {
	{22, 9},
};
static arc arcs_39_8[3] = {
	{95, 4},
	{91, 5},
	{0, 8},
};
static arc arcs_39_9[1] = {
	{0, 9},
};
static state states_39[10] = {
	{1, arcs_39_0},
	{1, arcs_39_1},
	{1, arcs_39_2},
	{2, arcs_39_3},
	{1, arcs_39_4},
	{1, arcs_39_5},
	{1, arcs_39_6},
	{1, arcs_39_7},
	{3, arcs_39_8},
	{1, arcs_39_9},
};
static arc arcs_40_0[1] = {
	{97, 1},
};
static arc arcs_40_1[2] = {
	{26, 2},
	{0, 1},
};
static arc arcs_40_2[2] = {
	{27, 3},
	{0, 2},
};
static arc arcs_40_3[1] = {
	{26, 4},
};
static arc arcs_40_4[1] = {
	{0, 4},
};
static state states_40[5] = {
	{1, arcs_40_0},
	{2, arcs_40_1},
	{2, arcs_40_2},
	{1, arcs_40_3},
	{1, arcs_40_4},
};
static arc arcs_41_0[2] = {
	{3, 1},
	{2, 2},
};
static arc arcs_41_1[1] = {
	{0, 1},
};
static arc arcs_41_2[1] = {
	{98, 3},
};
static arc arcs_41_3[1] = {
	{6, 4},
};
static arc arcs_41_4[2] = {
	{6, 4},
	{99, 1},
};
static state states_41[5] = {
	{2, arcs_41_0},
	{1, arcs_41_1},
	{1, arcs_41_2},
	{1, arcs_41_3},
	{2, arcs_41_4},
};
static arc arcs_42_0[2] = {
	{100, 1},
	{102, 2},
};
static arc arcs_42_1[2] = {
	{101, 3},
	{0, 1},
};
static arc arcs_42_2[1] = {
	{0, 2},
};
static arc arcs_42_3[1] = {
	{100, 1},
};
static state states_42[4] = {
	{2, arcs_42_0},
	{2, arcs_42_1},
	{1, arcs_42_2},
	{1, arcs_42_3},
};
static arc arcs_43_0[1] = {
	{103, 1},
};
static arc arcs_43_1[2] = {
	{104, 0},
	{0, 1},
};
static state states_43[2] = {
	{1, arcs_43_0},
	{2, arcs_43_1},
};
static arc arcs_44_0[2] = {
	{105, 1},
	{106, 2},
};
static arc arcs_44_1[1] = {
	{103, 2},
};
static arc arcs_44_2[1] = {
	{0, 2},
};
static state states_44[3] = {
	{2, arcs_44_0},
	{1, arcs_44_1},
	{1, arcs_44_2},
};
static arc arcs_45_0[1] = {
	{81, 1},
};
static arc arcs_45_1[2] = {
	{107, 0},
	{0, 1},
};
static state states_45[2] = {
	{1, arcs_45_0},
	{2, arcs_45_1},
};
static arc arcs_46_0[10] = {
	{108, 1},
	{109, 1},
	{110, 1},
	{111, 1},
	{112, 1},
	{113, 1},
	{114, 1},
	{82, 1},
	{105, 2},
	{115, 3},
};
static arc arcs_46_1[1] = {
	{0, 1},
};
static arc arcs_46_2[1] = {
	{82, 1},
};
static arc arcs_46_3[2] = {
	{105, 1},
	{0, 3},
};
static state states_46[4] = {
	{10, arcs_46_0},
	{1, arcs_46_1},
	{1, arcs_46_2},
	{2, arcs_46_3},
};
static arc arcs_47_0[1] = {
	{116, 1},
};
static arc arcs_47_1[2] = {
	{117, 0},
	{0, 1},
};
static state states_47[2] = {
	{1, arcs_47_0},
	{2, arcs_47_1},
};
static arc arcs_48_0[1] = {
	{118, 1},
};
static arc arcs_48_1[2] = {
	{119, 0},
	{0, 1},
};
static state states_48[2] = {
	{1, arcs_48_0},
	{2, arcs_48_1},
};
static arc arcs_49_0[1] = {
	{120, 1},
};
static arc arcs_49_1[2] = {
	{121, 0},
	{0, 1},
};
static state states_49[2] = {
	{1, arcs_49_0},
	{2, arcs_49_1},
};
static arc arcs_50_0[1] = {
	{122, 1},
};
static arc arcs_50_1[3] = {
	{123, 0},
	{56, 0},
	{0, 1},
};
static state states_50[2] = {
	{1, arcs_50_0},
	{3, arcs_50_1},
};
static arc arcs_51_0[1] = {
	{124, 1},
};
static arc arcs_51_1[3] = {
	{125, 0},
	{126, 0},
	{0, 1},
};
static state states_51[2] = {
	{1, arcs_51_0},
	{3, arcs_51_1},
};
static arc arcs_52_0[1] = {
	{127, 1},
};
static arc arcs_52_1[5] = {
	{28, 0},
	{128, 0},
	{129, 0},
	{130, 0},
	{0, 1},
};
static state states_52[2] = {
	{1, arcs_52_0},
	{5, arcs_52_1},
};
static arc arcs_53_0[4] = {
	{125, 1},
	{126, 1},
	{131, 1},
	{132, 2},
};
static arc arcs_53_1[1] = {
	{127, 2},
};
static arc arcs_53_2[1] = {
	{0, 2},
};
static state states_53[3] = {
	{4, arcs_53_0},
	{1, arcs_53_1},
	{1, arcs_53_2},
};
static arc arcs_54_0[1] = {
	{133, 1},
};
static arc arcs_54_1[3] = {
	{134, 1},
	{29, 2},
	{0, 1},
};
static arc arcs_54_2[1] = {
	{127, 3},
};
static arc arcs_54_3[1] = {
	{0, 3},
};
static state states_54[4] = {
	{1, arcs_54_0},
	{3, arcs_54_1},
	{1, arcs_54_2},
	{1, arcs_54_3},
};
static arc arcs_55_0[7] = {
	{13, 1},
	{136, 2},
	{139, 3},
	{142, 4},
	{19, 5},
	{144, 5},
	{145, 6},
};
static arc arcs_55_1[2] = {
	{135, 7},
	{15, 5},
};
static arc arcs_55_2[2] = {
	{137, 8},
	{138, 5},
};
static arc arcs_55_3[2] = {
	{140, 9},
	{141, 5},
};
static arc arcs_55_4[1] = {
	{143, 10},
};
static arc arcs_55_5[1] = {
	{0, 5},
};
static arc arcs_55_6[2] = {
	{145, 6},
	{0, 6},
};
static arc arcs_55_7[1] = {
	{15, 5},
};
static arc arcs_55_8[1] = {
	{138, 5},
};
static arc arcs_55_9[1] = {
	{141, 5},
};
static arc arcs_55_10[1] = {
	{142, 5},
};
static state states_55[11] = {
	{7, arcs_55_0},
	{2, arcs_55_1},
	{2, arcs_55_2},
	{2, arcs_55_3},
	{1, arcs_55_4},
	{1, arcs_55_5},
	{2, arcs_55_6},
	{1, arcs_55_7},
	{1, arcs_55_8},
	{1, arcs_55_9},
	{1, arcs_55_10},
};
static arc arcs_56_0[1] = {
	{26, 1},
};
static arc arcs_56_1[3] = {
	{146, 2},
	{27, 3},
	{0, 1},
};
static arc arcs_56_2[1] = {
	{0, 2},
};
static arc arcs_56_3[2] = {
	{26, 4},
	{0, 3},
};
static arc arcs_56_4[2] = {
	{27, 3},
	{0, 4},
};
static state states_56[5] = {
	{1, arcs_56_0},
	{3, arcs_56_1},
	{1, arcs_56_2},
	{2, arcs_56_3},
	{2, arcs_56_4},
};
static arc arcs_57_0[1] = {
	{26, 1},
};
static arc arcs_57_1[3] = {
	{147, 2},
	{27, 3},
	{0, 1},
};
static arc arcs_57_2[1] = {
	{0, 2},
};
static arc arcs_57_3[2] = {
	{26, 4},
	{0, 3},
};
static arc arcs_57_4[2] = {
	{27, 3},
	{0, 4},
};
static state states_57[5] = {
	{1, arcs_57_0},
	{3, arcs_57_1},
	{1, arcs_57_2},
	{2, arcs_57_3},
	{2, arcs_57_4},
};
static arc arcs_58_0[1] = {
	{148, 1},
};
static arc arcs_58_1[2] = {
	{23, 2},
	{21, 3},
};
static arc arcs_58_2[1] = {
	{21, 3},
};
static arc arcs_58_3[1] = {
	{26, 4},
};
static arc arcs_58_4[1] = {
	{0, 4},
};
static state states_58[5] = {
	{1, arcs_58_0},
	{2, arcs_58_1},
	{1, arcs_58_2},
	{1, arcs_58_3},
	{1, arcs_58_4},
};
static arc arcs_59_0[3] = {
	{13, 1},
	{136, 2},
	{78, 3},
};
static arc arcs_59_1[2] = {
	{14, 4},
	{15, 5},
};
static arc arcs_59_2[1] = {
	{149, 6},
};
static arc arcs_59_3[1] = {
	{19, 5},
};
static arc arcs_59_4[1] = {
	{15, 5},
};
static arc arcs_59_5[1] = {
	{0, 5},
};
static arc arcs_59_6[1] = {
	{138, 5},
};
static state states_59[7] = {
	{3, arcs_59_0},
	{2, arcs_59_1},
	{1, arcs_59_2},
	{1, arcs_59_3},
	{1, arcs_59_4},
	{1, arcs_59_5},
	{1, arcs_59_6},
};
static arc arcs_60_0[1] = {
	{150, 1},
};
static arc arcs_60_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_60_2[2] = {
	{150, 1},
	{0, 2},
};
static state states_60[3] = {
	{1, arcs_60_0},
	{2, arcs_60_1},
	{2, arcs_60_2},
};
static arc arcs_61_0[3] = {
	{78, 1},
	{26, 2},
	{21, 3},
};
static arc arcs_61_1[1] = {
	{78, 4},
};
static arc arcs_61_2[2] = {
	{21, 3},
	{0, 2},
};
static arc arcs_61_3[3] = {
	{26, 5},
	{151, 6},
	{0, 3},
};
static arc arcs_61_4[1] = {
	{78, 6},
};
static arc arcs_61_5[2] = {
	{151, 6},
	{0, 5},
};
static arc arcs_61_6[1] = {
	{0, 6},
};
static state states_61[7] = {
	{3, arcs_61_0},
	{1, arcs_61_1},
	{2, arcs_61_2},
	{3, arcs_61_3},
	{1, arcs_61_4},
	{2, arcs_61_5},
	{1, arcs_61_6},
};
static arc arcs_62_0[1] = {
	{21, 1},
};
static arc arcs_62_1[2] = {
	{26, 2},
	{0, 1},
};
static arc arcs_62_2[1] = {
	{0, 2},
};
static state states_62[3] = {
	{1, arcs_62_0},
	{2, arcs_62_1},
	{1, arcs_62_2},
};
static arc arcs_63_0[1] = {
	{81, 1},
};
static arc arcs_63_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_63_2[2] = {
	{81, 1},
	{0, 2},
};
static state states_63[3] = {
	{1, arcs_63_0},
	{2, arcs_63_1},
	{2, arcs_63_2},
};
static arc arcs_64_0[1] = {
	{26, 1},
};
static arc arcs_64_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_64_2[2] = {
	{26, 1},
	{0, 2},
};
static state states_64[3] = {
	{1, arcs_64_0},
	{2, arcs_64_1},
	{2, arcs_64_2},
};
static arc arcs_65_0[1] = {
	{26, 1},
};
static arc arcs_65_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_65_2[1] = {
	{26, 3},
};
static arc arcs_65_3[2] = {
	{27, 4},
	{0, 3},
};
static arc arcs_65_4[2] = {
	{26, 3},
	{0, 4},
};
static state states_65[5] = {
	{1, arcs_65_0},
	{2, arcs_65_1},
	{1, arcs_65_2},
	{2, arcs_65_3},
	{2, arcs_65_4},
};
static arc arcs_66_0[1] = {
	{26, 1},
};
static arc arcs_66_1[1] = {
	{21, 2},
};
static arc arcs_66_2[1] = {
	{26, 3},
};
static arc arcs_66_3[2] = {
	{27, 4},
	{0, 3},
};
static arc arcs_66_4[2] = {
	{26, 1},
	{0, 4},
};
static state states_66[5] = {
	{1, arcs_66_0},
	{1, arcs_66_1},
	{1, arcs_66_2},
	{2, arcs_66_3},
	{2, arcs_66_4},
};
static arc arcs_67_0[1] = {
	{153, 1},
};
static arc arcs_67_1[1] = {
	{19, 2},
};
static arc arcs_67_2[2] = {
	{13, 3},
	{21, 4},
};
static arc arcs_67_3[1] = {
	{9, 5},
};
static arc arcs_67_4[1] = {
	{22, 6},
};
static arc arcs_67_5[1] = {
	{15, 7},
};
static arc arcs_67_6[1] = {
	{0, 6},
};
static arc arcs_67_7[1] = {
	{21, 4},
};
static state states_67[8] = {
	{1, arcs_67_0},
	{1, arcs_67_1},
	{2, arcs_67_2},
	{1, arcs_67_3},
	{1, arcs_67_4},
	{1, arcs_67_5},
	{1, arcs_67_6},
	{1, arcs_67_7},
};
static arc arcs_68_0[3] = {
	{154, 1},
	{28, 2},
	{29, 3},
};
static arc arcs_68_1[2] = {
	{27, 4},
	{0, 1},
};
static arc arcs_68_2[1] = {
	{26, 5},
};
static arc arcs_68_3[1] = {
	{26, 6},
};
static arc arcs_68_4[4] = {
	{154, 1},
	{28, 2},
	{29, 3},
	{0, 4},
};
static arc arcs_68_5[2] = {
	{27, 7},
	{0, 5},
};
static arc arcs_68_6[1] = {
	{0, 6},
};
static arc arcs_68_7[1] = {
	{29, 3},
};
static state states_68[8] = {
	{3, arcs_68_0},
	{2, arcs_68_1},
	{1, arcs_68_2},
	{1, arcs_68_3},
	{4, arcs_68_4},
	{2, arcs_68_5},
	{1, arcs_68_6},
	{1, arcs_68_7},
};
static arc arcs_69_0[1] = {
	{26, 1},
};
static arc arcs_69_1[3] = {
	{147, 2},
	{25, 3},
	{0, 1},
};
static arc arcs_69_2[1] = {
	{0, 2},
};
static arc arcs_69_3[1] = {
	{26, 4},
};
static arc arcs_69_4[2] = {
	{13, 5},
	{0, 4},
};
static arc arcs_69_5[1] = {
	{147, 6},
};
static arc arcs_69_6[1] = {
	{15, 2},
};
static state states_69[7] = {
	{1, arcs_69_0},
	{3, arcs_69_1},
	{1, arcs_69_2},
	{1, arcs_69_3},
	{2, arcs_69_4},
	{1, arcs_69_5},
	{1, arcs_69_6},
};
static arc arcs_70_0[2] = {
	{146, 1},
	{156, 1},
};
static arc arcs_70_1[1] = {
	{0, 1},
};
static state states_70[2] = {
	{2, arcs_70_0},
	{1, arcs_70_1},
};
static arc arcs_71_0[1] = {
	{93, 1},
};
static arc arcs_71_1[1] = {
	{58, 2},
};
static arc arcs_71_2[1] = {
	{82, 3},
};
static arc arcs_71_3[1] = {
	{152, 4},
};
static arc arcs_71_4[2] = {
	{155, 5},
	{0, 4},
};
static arc arcs_71_5[1] = {
	{0, 5},
};
static state states_71[6] = {
	{1, arcs_71_0},
	{1, arcs_71_1},
	{1, arcs_71_2},
	{1, arcs_71_3},
	{2, arcs_71_4},
	{1, arcs_71_5},
};
static arc arcs_72_0[1] = {
	{89, 1},
};
static arc arcs_72_1[1] = {
	{26, 2},
};
static arc arcs_72_2[2] = {
	{155, 3},
	{0, 2},
};
static arc arcs_72_3[1] = {
	{0, 3},
};
static state states_72[4] = {
	{1, arcs_72_0},
	{1, arcs_72_1},
	{2, arcs_72_2},
	{1, arcs_72_3},
};
static arc arcs_73_0[2] = {
	{147, 1},
	{158, 1},
};
static arc arcs_73_1[1] = {
	{0, 1},
};
static state states_73[2] = {
	{2, arcs_73_0},
	{1, arcs_73_1},
};
static arc arcs_74_0[1] = {
	{93, 1},
};
static arc arcs_74_1[1] = {
	{58, 2},
};
static arc arcs_74_2[1] = {
	{82, 3},
};
static arc arcs_74_3[1] = {
	{26, 4},
};
static arc arcs_74_4[2] = {
	{157, 5},
	{0, 4},
};
static arc arcs_74_5[1] = {
	{0, 5},
};
static state states_74[6] = {
	{1, arcs_74_0},
	{1, arcs_74_1},
	{1, arcs_74_2},
	{1, arcs_74_3},
	{2, arcs_74_4},
	{1, arcs_74_5},
};
static arc arcs_75_0[1] = {
	{89, 1},
};
static arc arcs_75_1[1] = {
	{26, 2},
};
static arc arcs_75_2[2] = {
	{157, 3},
	{0, 2},
};
static arc arcs_75_3[1] = {
	{0, 3},
};
static state states_75[4] = {
	{1, arcs_75_0},
	{1, arcs_75_1},
	{2, arcs_75_2},
	{1, arcs_75_3},
};
static arc arcs_76_0[1] = {
	{26, 1},
};
static arc arcs_76_1[2] = {
	{27, 0},
	{0, 1},
};
static state states_76[2] = {
	{1, arcs_76_0},
	{2, arcs_76_1},
};
static arc arcs_77_0[1] = {
	{19, 1},
};
static arc arcs_77_1[1] = {
	{0, 1},
};
static state states_77[2] = {
	{1, arcs_77_0},
	{1, arcs_77_1},
};
static dfa dfas[78] = {
	{256, "single_input", 0, 3, states_0,
	 "\004\050\014\000\000\000\200\012\076\205\011\162\000\002\000\140\010\111\023\002"},
	{257, "file_input", 0, 2, states_1,
	 "\204\050\014\000\000\000\200\012\076\205\011\162\000\002\000\140\010\111\023\002"},
	{258, "eval_input", 0, 3, states_2,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\023\000"},
	{259, "decorator", 0, 7, states_3,
	 "\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{260, "decorators", 0, 2, states_4,
	 "\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{261, "funcdef", 0, 7, states_5,
	 "\000\010\004\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{262, "parameters", 0, 4, states_6,
	 "\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{263, "varargslist", 0, 10, states_7,
	 "\000\040\010\060\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{264, "fpdef", 0, 4, states_8,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{265, "fplist", 0, 3, states_9,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{266, "stmt", 0, 2, states_10,
	 "\000\050\014\000\000\000\200\012\076\205\011\162\000\002\000\140\010\111\023\002"},
	{267, "simple_stmt", 0, 4, states_11,
	 "\000\040\010\000\000\000\200\012\076\205\011\000\000\002\000\140\010\111\023\000"},
	{268, "small_stmt", 0, 2, states_12,
	 "\000\040\010\000\000\000\200\012\076\205\011\000\000\002\000\140\010\111\023\000"},
	{269, "expr_stmt", 0, 6, states_13,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\023\000"},
	{270, "augassign", 0, 2, states_14,
	 "\000\000\000\000\000\370\177\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{271, "print_stmt", 0, 9, states_15,
	 "\000\000\000\000\000\000\200\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{272, "del_stmt", 0, 3, states_16,
	 "\000\000\000\000\000\000\000\002\000\000\000\000\000\000\000\000\000\000\000\000"},
	{273, "pass_stmt", 0, 2, states_17,
	 "\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000"},
	{274, "flow_stmt", 0, 2, states_18,
	 "\000\000\000\000\000\000\000\000\076\000\000\000\000\000\000\000\000\000\000\000"},
	{275, "break_stmt", 0, 2, states_19,
	 "\000\000\000\000\000\000\000\000\002\000\000\000\000\000\000\000\000\000\000\000"},
	{276, "continue_stmt", 0, 2, states_20,
	 "\000\000\000\000\000\000\000\000\004\000\000\000\000\000\000\000\000\000\000\000"},
	{277, "return_stmt", 0, 3, states_21,
	 "\000\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000\000\000\000"},
	{278, "yield_stmt", 0, 3, states_22,
	 "\000\000\000\000\000\000\000\000\020\000\000\000\000\000\000\000\000\000\000\000"},
	{279, "raise_stmt", 0, 7, states_23,
	 "\000\000\000\000\000\000\000\000\040\000\000\000\000\000\000\000\000\000\000\000"},
	{280, "import_stmt", 0, 2, states_24,
	 "\000\000\000\000\000\000\000\000\000\005\000\000\000\000\000\000\000\000\000\000"},
	{281, "import_name", 0, 3, states_25,
	 "\000\000\000\000\000\000\000\000\000\001\000\000\000\000\000\000\000\000\000\000"},
	{282, "import_from", 0, 7, states_26,
	 "\000\000\000\000\000\000\000\000\000\004\000\000\000\000\000\000\000\000\000\000"},
	{283, "import_as_name", 0, 4, states_27,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{284, "dotted_as_name", 0, 4, states_28,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{285, "import_as_names", 0, 3, states_29,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{286, "dotted_as_names", 0, 2, states_30,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{287, "dotted_name", 0, 2, states_31,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{288, "global_stmt", 0, 3, states_32,
	 "\000\000\000\000\000\000\000\000\000\200\000\000\000\000\000\000\000\000\000\000"},
	{289, "exec_stmt", 0, 7, states_33,
	 "\000\000\000\000\000\000\000\000\000\000\001\000\000\000\000\000\000\000\000\000"},
	{290, "assert_stmt", 0, 5, states_34,
	 "\000\000\000\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000\000"},
	{291, "compound_stmt", 0, 2, states_35,
	 "\000\010\004\000\000\000\000\000\000\000\000\162\000\000\000\000\000\000\000\002"},
	{292, "if_stmt", 0, 8, states_36,
	 "\000\000\000\000\000\000\000\000\000\000\000\002\000\000\000\000\000\000\000\000"},
	{293, "while_stmt", 0, 8, states_37,
	 "\000\000\000\000\000\000\000\000\000\000\000\020\000\000\000\000\000\000\000\000"},
	{294, "for_stmt", 0, 10, states_38,
	 "\000\000\000\000\000\000\000\000\000\000\000\040\000\000\000\000\000\000\000\000"},
	{295, "try_stmt", 0, 10, states_39,
	 "\000\000\000\000\000\000\000\000\000\000\000\100\000\000\000\000\000\000\000\000"},
	{296, "except_clause", 0, 5, states_40,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\002\000\000\000\000\000\000\000"},
	{297, "suite", 0, 5, states_41,
	 "\004\040\010\000\000\000\200\012\076\205\011\000\000\002\000\140\010\111\023\000"},
	{298, "test", 0, 4, states_42,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\023\000"},
	{299, "and_test", 0, 2, states_43,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\003\000"},
	{300, "not_test", 0, 3, states_44,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\003\000"},
	{301, "comparison", 0, 2, states_45,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\140\010\111\003\000"},
	{302, "comp_op", 0, 4, states_46,
	 "\000\000\000\000\000\000\000\000\000\000\004\000\000\362\017\000\000\000\000\000"},
	{303, "expr", 0, 2, states_47,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\140\010\111\003\000"},
	{304, "xor_expr", 0, 2, states_48,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\140\010\111\003\000"},
	{305, "and_expr", 0, 2, states_49,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\140\010\111\003\000"},
	{306, "shift_expr", 0, 2, states_50,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\140\010\111\003\000"},
	{307, "arith_expr", 0, 2, states_51,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\140\010\111\003\000"},
	{308, "term", 0, 2, states_52,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\140\010\111\003\000"},
	{309, "factor", 0, 3, states_53,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\140\010\111\003\000"},
	{310, "power", 0, 4, states_54,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\111\003\000"},
	{311, "atom", 0, 11, states_55,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\111\003\000"},
	{312, "listmaker", 0, 5, states_56,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\023\000"},
	{313, "testlist_gexp", 0, 5, states_57,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\023\000"},
	{314, "lambdef", 0, 5, states_58,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\020\000"},
	{315, "trailer", 0, 7, states_59,
	 "\000\040\000\000\000\000\000\000\000\100\000\000\000\000\000\000\000\001\000\000"},
	{316, "subscriptlist", 0, 3, states_60,
	 "\000\040\050\000\000\000\000\000\000\100\000\000\000\002\000\140\010\111\023\000"},
	{317, "subscript", 0, 7, states_61,
	 "\000\040\050\000\000\000\000\000\000\100\000\000\000\002\000\140\010\111\023\000"},
	{318, "sliceop", 0, 3, states_62,
	 "\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{319, "exprlist", 0, 3, states_63,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\140\010\111\003\000"},
	{320, "testlist", 0, 3, states_64,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\023\000"},
	{321, "testlist_safe", 0, 5, states_65,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\023\000"},
	{322, "dictmaker", 0, 5, states_66,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\023\000"},
	{323, "classdef", 0, 8, states_67,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\002"},
	{324, "arglist", 0, 8, states_68,
	 "\000\040\010\060\000\000\000\000\000\000\000\000\000\002\000\140\010\111\023\000"},
	{325, "argument", 0, 7, states_69,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\023\000"},
	{326, "list_iter", 0, 2, states_70,
	 "\000\000\000\000\000\000\000\000\000\000\000\042\000\000\000\000\000\000\000\000"},
	{327, "list_for", 0, 6, states_71,
	 "\000\000\000\000\000\000\000\000\000\000\000\040\000\000\000\000\000\000\000\000"},
	{328, "list_if", 0, 4, states_72,
	 "\000\000\000\000\000\000\000\000\000\000\000\002\000\000\000\000\000\000\000\000"},
	{329, "gen_iter", 0, 2, states_73,
	 "\000\000\000\000\000\000\000\000\000\000\000\042\000\000\000\000\000\000\000\000"},
	{330, "gen_for", 0, 6, states_74,
	 "\000\000\000\000\000\000\000\000\000\000\000\040\000\000\000\000\000\000\000\000"},
	{331, "gen_if", 0, 4, states_75,
	 "\000\000\000\000\000\000\000\000\000\000\000\002\000\000\000\000\000\000\000\000"},
	{332, "testlist1", 0, 2, states_76,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\002\000\140\010\111\023\000"},
	{333, "encoding_decl", 0, 2, states_77,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
};
static label labels[160] = {
	{0, "EMPTY"},
	{256, 0},
	{4, 0},
	{267, 0},
	{291, 0},
	{257, 0},
	{266, 0},
	{0, 0},
	{258, 0},
	{320, 0},
	{259, 0},
	{50, 0},
	{287, 0},
	{7, 0},
	{324, 0},
	{8, 0},
	{260, 0},
	{261, 0},
	{1, "def"},
	{1, 0},
	{262, 0},
	{11, 0},
	{297, 0},
	{263, 0},
	{264, 0},
	{22, 0},
	{298, 0},
	{12, 0},
	{16, 0},
	{36, 0},
	{265, 0},
	{268, 0},
	{13, 0},
	{269, 0},
	{271, 0},
	{272, 0},
	{273, 0},
	{274, 0},
	{280, 0},
	{288, 0},
	{289, 0},
	{290, 0},
	{270, 0},
	{37, 0},
	{38, 0},
	{39, 0},
	{40, 0},
	{41, 0},
	{42, 0},
	{43, 0},
	{44, 0},
	{45, 0},
	{46, 0},
	{47, 0},
	{49, 0},
	{1, "print"},
	{35, 0},
	{1, "del"},
	{319, 0},
	{1, "pass"},
	{275, 0},
	{276, 0},
	{277, 0},
	{279, 0},
	{278, 0},
	{1, "break"},
	{1, "continue"},
	{1, "return"},
	{1, "yield"},
	{1, "raise"},
	{281, 0},
	{282, 0},
	{1, "import"},
	{286, 0},
	{1, "from"},
	{285, 0},
	{283, 0},
	{284, 0},
	{23, 0},
	{1, "global"},
	{1, "exec"},
	{303, 0},
	{1, "in"},
	{1, "assert"},
	{292, 0},
	{293, 0},
	{294, 0},
	{295, 0},
	{323, 0},
	{1, "if"},
	{1, "elif"},
	{1, "else"},
	{1, "while"},
	{1, "for"},
	{1, "try"},
	{296, 0},
	{1, "finally"},
	{1, "except"},
	{5, 0},
	{6, 0},
	{299, 0},
	{1, "or"},
	{314, 0},
	{300, 0},
	{1, "and"},
	{1, "not"},
	{301, 0},
	{302, 0},
	{20, 0},
	{21, 0},
	{28, 0},
	{31, 0},
	{30, 0},
	{29, 0},
	{29, 0},
	{1, "is"},
	{304, 0},
	{18, 0},
	{305, 0},
	{33, 0},
	{306, 0},
	{19, 0},
	{307, 0},
	{34, 0},
	{308, 0},
	{14, 0},
	{15, 0},
	{309, 0},
	{17, 0},
	{24, 0},
	{48, 0},
	{32, 0},
	{310, 0},
	{311, 0},
	{315, 0},
	{313, 0},
	{9, 0},
	{312, 0},
	{10, 0},
	{26, 0},
	{322, 0},
	{27, 0},
	{25, 0},
	{332, 0},
	{2, 0},
	{3, 0},
	{327, 0},
	{330, 0},
	{1, "lambda"},
	{316, 0},
	{317, 0},
	{318, 0},
	{321, 0},
	{1, "class"},
	{325, 0},
	{326, 0},
	{328, 0},
	{329, 0},
	{331, 0},
	{333, 0},
};
grammar _PyParser_Grammar = {
	78,
	dfas,
	{160, labels},
	256
};
