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
static arc arcs_5_0[1] = {
	{16, 1},
};
static arc arcs_5_1[2] = {
	{18, 2},
	{19, 2},
};
static arc arcs_5_2[1] = {
	{0, 2},
};
static state states_5[3] = {
	{1, arcs_5_0},
	{2, arcs_5_1},
	{1, arcs_5_2},
};
static arc arcs_6_0[1] = {
	{20, 1},
};
static arc arcs_6_1[1] = {
	{21, 2},
};
static arc arcs_6_2[1] = {
	{22, 3},
};
static arc arcs_6_3[2] = {
	{23, 4},
	{25, 5},
};
static arc arcs_6_4[1] = {
	{24, 6},
};
static arc arcs_6_5[1] = {
	{26, 7},
};
static arc arcs_6_6[1] = {
	{25, 5},
};
static arc arcs_6_7[1] = {
	{0, 7},
};
static state states_6[8] = {
	{1, arcs_6_0},
	{1, arcs_6_1},
	{1, arcs_6_2},
	{2, arcs_6_3},
	{1, arcs_6_4},
	{1, arcs_6_5},
	{1, arcs_6_6},
	{1, arcs_6_7},
};
static arc arcs_7_0[1] = {
	{13, 1},
};
static arc arcs_7_1[2] = {
	{27, 2},
	{15, 3},
};
static arc arcs_7_2[1] = {
	{15, 3},
};
static arc arcs_7_3[1] = {
	{0, 3},
};
static state states_7[4] = {
	{1, arcs_7_0},
	{2, arcs_7_1},
	{1, arcs_7_2},
	{1, arcs_7_3},
};
static arc arcs_8_0[3] = {
	{28, 1},
	{31, 2},
	{32, 3},
};
static arc arcs_8_1[3] = {
	{29, 4},
	{30, 5},
	{0, 1},
};
static arc arcs_8_2[3] = {
	{28, 6},
	{30, 7},
	{0, 2},
};
static arc arcs_8_3[1] = {
	{28, 8},
};
static arc arcs_8_4[1] = {
	{24, 9},
};
static arc arcs_8_5[4] = {
	{28, 1},
	{31, 2},
	{32, 3},
	{0, 5},
};
static arc arcs_8_6[2] = {
	{30, 7},
	{0, 6},
};
static arc arcs_8_7[2] = {
	{28, 10},
	{32, 3},
};
static arc arcs_8_8[1] = {
	{0, 8},
};
static arc arcs_8_9[2] = {
	{30, 5},
	{0, 9},
};
static arc arcs_8_10[3] = {
	{30, 7},
	{29, 11},
	{0, 10},
};
static arc arcs_8_11[1] = {
	{24, 6},
};
static state states_8[12] = {
	{3, arcs_8_0},
	{3, arcs_8_1},
	{3, arcs_8_2},
	{1, arcs_8_3},
	{1, arcs_8_4},
	{4, arcs_8_5},
	{2, arcs_8_6},
	{2, arcs_8_7},
	{1, arcs_8_8},
	{2, arcs_8_9},
	{3, arcs_8_10},
	{1, arcs_8_11},
};
static arc arcs_9_0[1] = {
	{21, 1},
};
static arc arcs_9_1[2] = {
	{25, 2},
	{0, 1},
};
static arc arcs_9_2[1] = {
	{24, 3},
};
static arc arcs_9_3[1] = {
	{0, 3},
};
static state states_9[4] = {
	{1, arcs_9_0},
	{2, arcs_9_1},
	{1, arcs_9_2},
	{1, arcs_9_3},
};
static arc arcs_10_0[3] = {
	{34, 1},
	{31, 2},
	{32, 3},
};
static arc arcs_10_1[3] = {
	{29, 4},
	{30, 5},
	{0, 1},
};
static arc arcs_10_2[3] = {
	{34, 6},
	{30, 7},
	{0, 2},
};
static arc arcs_10_3[1] = {
	{34, 8},
};
static arc arcs_10_4[1] = {
	{24, 9},
};
static arc arcs_10_5[4] = {
	{34, 1},
	{31, 2},
	{32, 3},
	{0, 5},
};
static arc arcs_10_6[2] = {
	{30, 7},
	{0, 6},
};
static arc arcs_10_7[2] = {
	{34, 10},
	{32, 3},
};
static arc arcs_10_8[1] = {
	{0, 8},
};
static arc arcs_10_9[2] = {
	{30, 5},
	{0, 9},
};
static arc arcs_10_10[3] = {
	{30, 7},
	{29, 11},
	{0, 10},
};
static arc arcs_10_11[1] = {
	{24, 6},
};
static state states_10[12] = {
	{3, arcs_10_0},
	{3, arcs_10_1},
	{3, arcs_10_2},
	{1, arcs_10_3},
	{1, arcs_10_4},
	{4, arcs_10_5},
	{2, arcs_10_6},
	{2, arcs_10_7},
	{1, arcs_10_8},
	{2, arcs_10_9},
	{3, arcs_10_10},
	{1, arcs_10_11},
};
static arc arcs_11_0[1] = {
	{21, 1},
};
static arc arcs_11_1[1] = {
	{0, 1},
};
static state states_11[2] = {
	{1, arcs_11_0},
	{1, arcs_11_1},
};
static arc arcs_12_0[2] = {
	{3, 1},
	{4, 1},
};
static arc arcs_12_1[1] = {
	{0, 1},
};
static state states_12[2] = {
	{2, arcs_12_0},
	{1, arcs_12_1},
};
static arc arcs_13_0[1] = {
	{35, 1},
};
static arc arcs_13_1[2] = {
	{36, 2},
	{2, 3},
};
static arc arcs_13_2[2] = {
	{35, 1},
	{2, 3},
};
static arc arcs_13_3[1] = {
	{0, 3},
};
static state states_13[4] = {
	{1, arcs_13_0},
	{2, arcs_13_1},
	{2, arcs_13_2},
	{1, arcs_13_3},
};
static arc arcs_14_0[8] = {
	{37, 1},
	{38, 1},
	{39, 1},
	{40, 1},
	{41, 1},
	{42, 1},
	{43, 1},
	{44, 1},
};
static arc arcs_14_1[1] = {
	{0, 1},
};
static state states_14[2] = {
	{8, arcs_14_0},
	{1, arcs_14_1},
};
static arc arcs_15_0[1] = {
	{9, 1},
};
static arc arcs_15_1[3] = {
	{45, 2},
	{29, 3},
	{0, 1},
};
static arc arcs_15_2[2] = {
	{46, 4},
	{9, 4},
};
static arc arcs_15_3[2] = {
	{46, 5},
	{9, 5},
};
static arc arcs_15_4[1] = {
	{0, 4},
};
static arc arcs_15_5[2] = {
	{29, 3},
	{0, 5},
};
static state states_15[6] = {
	{1, arcs_15_0},
	{3, arcs_15_1},
	{2, arcs_15_2},
	{2, arcs_15_3},
	{1, arcs_15_4},
	{2, arcs_15_5},
};
static arc arcs_16_0[12] = {
	{47, 1},
	{48, 1},
	{49, 1},
	{50, 1},
	{51, 1},
	{52, 1},
	{53, 1},
	{54, 1},
	{55, 1},
	{56, 1},
	{57, 1},
	{58, 1},
};
static arc arcs_16_1[1] = {
	{0, 1},
};
static state states_16[2] = {
	{12, arcs_16_0},
	{1, arcs_16_1},
};
static arc arcs_17_0[1] = {
	{59, 1},
};
static arc arcs_17_1[1] = {
	{60, 2},
};
static arc arcs_17_2[1] = {
	{0, 2},
};
static state states_17[3] = {
	{1, arcs_17_0},
	{1, arcs_17_1},
	{1, arcs_17_2},
};
static arc arcs_18_0[1] = {
	{61, 1},
};
static arc arcs_18_1[1] = {
	{0, 1},
};
static state states_18[2] = {
	{1, arcs_18_0},
	{1, arcs_18_1},
};
static arc arcs_19_0[5] = {
	{62, 1},
	{63, 1},
	{64, 1},
	{65, 1},
	{66, 1},
};
static arc arcs_19_1[1] = {
	{0, 1},
};
static state states_19[2] = {
	{5, arcs_19_0},
	{1, arcs_19_1},
};
static arc arcs_20_0[1] = {
	{67, 1},
};
static arc arcs_20_1[1] = {
	{0, 1},
};
static state states_20[2] = {
	{1, arcs_20_0},
	{1, arcs_20_1},
};
static arc arcs_21_0[1] = {
	{68, 1},
};
static arc arcs_21_1[1] = {
	{0, 1},
};
static state states_21[2] = {
	{1, arcs_21_0},
	{1, arcs_21_1},
};
static arc arcs_22_0[1] = {
	{69, 1},
};
static arc arcs_22_1[2] = {
	{9, 2},
	{0, 1},
};
static arc arcs_22_2[1] = {
	{0, 2},
};
static state states_22[3] = {
	{1, arcs_22_0},
	{2, arcs_22_1},
	{1, arcs_22_2},
};
static arc arcs_23_0[1] = {
	{46, 1},
};
static arc arcs_23_1[1] = {
	{0, 1},
};
static state states_23[2] = {
	{1, arcs_23_0},
	{1, arcs_23_1},
};
static arc arcs_24_0[1] = {
	{70, 1},
};
static arc arcs_24_1[2] = {
	{24, 2},
	{0, 1},
};
static arc arcs_24_2[2] = {
	{71, 3},
	{0, 2},
};
static arc arcs_24_3[1] = {
	{24, 4},
};
static arc arcs_24_4[1] = {
	{0, 4},
};
static state states_24[5] = {
	{1, arcs_24_0},
	{2, arcs_24_1},
	{2, arcs_24_2},
	{1, arcs_24_3},
	{1, arcs_24_4},
};
static arc arcs_25_0[2] = {
	{72, 1},
	{73, 1},
};
static arc arcs_25_1[1] = {
	{0, 1},
};
static state states_25[2] = {
	{2, arcs_25_0},
	{1, arcs_25_1},
};
static arc arcs_26_0[1] = {
	{74, 1},
};
static arc arcs_26_1[1] = {
	{75, 2},
};
static arc arcs_26_2[1] = {
	{0, 2},
};
static state states_26[3] = {
	{1, arcs_26_0},
	{1, arcs_26_1},
	{1, arcs_26_2},
};
static arc arcs_27_0[1] = {
	{71, 1},
};
static arc arcs_27_1[3] = {
	{76, 2},
	{77, 2},
	{12, 3},
};
static arc arcs_27_2[4] = {
	{76, 2},
	{77, 2},
	{12, 3},
	{74, 4},
};
static arc arcs_27_3[1] = {
	{74, 4},
};
static arc arcs_27_4[3] = {
	{31, 5},
	{13, 6},
	{78, 5},
};
static arc arcs_27_5[1] = {
	{0, 5},
};
static arc arcs_27_6[1] = {
	{78, 7},
};
static arc arcs_27_7[1] = {
	{15, 5},
};
static state states_27[8] = {
	{1, arcs_27_0},
	{3, arcs_27_1},
	{4, arcs_27_2},
	{1, arcs_27_3},
	{3, arcs_27_4},
	{1, arcs_27_5},
	{1, arcs_27_6},
	{1, arcs_27_7},
};
static arc arcs_28_0[1] = {
	{21, 1},
};
static arc arcs_28_1[2] = {
	{80, 2},
	{0, 1},
};
static arc arcs_28_2[1] = {
	{21, 3},
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
	{12, 1},
};
static arc arcs_29_1[2] = {
	{80, 2},
	{0, 1},
};
static arc arcs_29_2[1] = {
	{21, 3},
};
static arc arcs_29_3[1] = {
	{0, 3},
};
static state states_29[4] = {
	{1, arcs_29_0},
	{2, arcs_29_1},
	{1, arcs_29_2},
	{1, arcs_29_3},
};
static arc arcs_30_0[1] = {
	{79, 1},
};
static arc arcs_30_1[2] = {
	{30, 2},
	{0, 1},
};
static arc arcs_30_2[2] = {
	{79, 1},
	{0, 2},
};
static state states_30[3] = {
	{1, arcs_30_0},
	{2, arcs_30_1},
	{2, arcs_30_2},
};
static arc arcs_31_0[1] = {
	{81, 1},
};
static arc arcs_31_1[2] = {
	{30, 0},
	{0, 1},
};
static state states_31[2] = {
	{1, arcs_31_0},
	{2, arcs_31_1},
};
static arc arcs_32_0[1] = {
	{21, 1},
};
static arc arcs_32_1[2] = {
	{76, 0},
	{0, 1},
};
static state states_32[2] = {
	{1, arcs_32_0},
	{2, arcs_32_1},
};
static arc arcs_33_0[1] = {
	{82, 1},
};
static arc arcs_33_1[1] = {
	{21, 2},
};
static arc arcs_33_2[2] = {
	{30, 1},
	{0, 2},
};
static state states_33[3] = {
	{1, arcs_33_0},
	{1, arcs_33_1},
	{2, arcs_33_2},
};
static arc arcs_34_0[1] = {
	{83, 1},
};
static arc arcs_34_1[1] = {
	{21, 2},
};
static arc arcs_34_2[2] = {
	{30, 1},
	{0, 2},
};
static state states_34[3] = {
	{1, arcs_34_0},
	{1, arcs_34_1},
	{2, arcs_34_2},
};
static arc arcs_35_0[1] = {
	{84, 1},
};
static arc arcs_35_1[1] = {
	{24, 2},
};
static arc arcs_35_2[2] = {
	{30, 3},
	{0, 2},
};
static arc arcs_35_3[1] = {
	{24, 4},
};
static arc arcs_35_4[1] = {
	{0, 4},
};
static state states_35[5] = {
	{1, arcs_35_0},
	{1, arcs_35_1},
	{2, arcs_35_2},
	{1, arcs_35_3},
	{1, arcs_35_4},
};
static arc arcs_36_0[8] = {
	{85, 1},
	{86, 1},
	{87, 1},
	{88, 1},
	{89, 1},
	{19, 1},
	{18, 1},
	{17, 1},
};
static arc arcs_36_1[1] = {
	{0, 1},
};
static state states_36[2] = {
	{8, arcs_36_0},
	{1, arcs_36_1},
};
static arc arcs_37_0[1] = {
	{90, 1},
};
static arc arcs_37_1[1] = {
	{24, 2},
};
static arc arcs_37_2[1] = {
	{25, 3},
};
static arc arcs_37_3[1] = {
	{26, 4},
};
static arc arcs_37_4[3] = {
	{91, 1},
	{92, 5},
	{0, 4},
};
static arc arcs_37_5[1] = {
	{25, 6},
};
static arc arcs_37_6[1] = {
	{26, 7},
};
static arc arcs_37_7[1] = {
	{0, 7},
};
static state states_37[8] = {
	{1, arcs_37_0},
	{1, arcs_37_1},
	{1, arcs_37_2},
	{1, arcs_37_3},
	{3, arcs_37_4},
	{1, arcs_37_5},
	{1, arcs_37_6},
	{1, arcs_37_7},
};
static arc arcs_38_0[1] = {
	{93, 1},
};
static arc arcs_38_1[1] = {
	{24, 2},
};
static arc arcs_38_2[1] = {
	{25, 3},
};
static arc arcs_38_3[1] = {
	{26, 4},
};
static arc arcs_38_4[2] = {
	{92, 5},
	{0, 4},
};
static arc arcs_38_5[1] = {
	{25, 6},
};
static arc arcs_38_6[1] = {
	{26, 7},
};
static arc arcs_38_7[1] = {
	{0, 7},
};
static state states_38[8] = {
	{1, arcs_38_0},
	{1, arcs_38_1},
	{1, arcs_38_2},
	{1, arcs_38_3},
	{2, arcs_38_4},
	{1, arcs_38_5},
	{1, arcs_38_6},
	{1, arcs_38_7},
};
static arc arcs_39_0[1] = {
	{94, 1},
};
static arc arcs_39_1[1] = {
	{60, 2},
};
static arc arcs_39_2[1] = {
	{95, 3},
};
static arc arcs_39_3[1] = {
	{9, 4},
};
static arc arcs_39_4[1] = {
	{25, 5},
};
static arc arcs_39_5[1] = {
	{26, 6},
};
static arc arcs_39_6[2] = {
	{92, 7},
	{0, 6},
};
static arc arcs_39_7[1] = {
	{25, 8},
};
static arc arcs_39_8[1] = {
	{26, 9},
};
static arc arcs_39_9[1] = {
	{0, 9},
};
static state states_39[10] = {
	{1, arcs_39_0},
	{1, arcs_39_1},
	{1, arcs_39_2},
	{1, arcs_39_3},
	{1, arcs_39_4},
	{1, arcs_39_5},
	{2, arcs_39_6},
	{1, arcs_39_7},
	{1, arcs_39_8},
	{1, arcs_39_9},
};
static arc arcs_40_0[1] = {
	{96, 1},
};
static arc arcs_40_1[1] = {
	{25, 2},
};
static arc arcs_40_2[1] = {
	{26, 3},
};
static arc arcs_40_3[2] = {
	{97, 4},
	{98, 5},
};
static arc arcs_40_4[1] = {
	{25, 6},
};
static arc arcs_40_5[1] = {
	{25, 7},
};
static arc arcs_40_6[1] = {
	{26, 8},
};
static arc arcs_40_7[1] = {
	{26, 9},
};
static arc arcs_40_8[4] = {
	{97, 4},
	{92, 10},
	{98, 5},
	{0, 8},
};
static arc arcs_40_9[1] = {
	{0, 9},
};
static arc arcs_40_10[1] = {
	{25, 11},
};
static arc arcs_40_11[1] = {
	{26, 12},
};
static arc arcs_40_12[2] = {
	{98, 5},
	{0, 12},
};
static state states_40[13] = {
	{1, arcs_40_0},
	{1, arcs_40_1},
	{1, arcs_40_2},
	{2, arcs_40_3},
	{1, arcs_40_4},
	{1, arcs_40_5},
	{1, arcs_40_6},
	{1, arcs_40_7},
	{4, arcs_40_8},
	{1, arcs_40_9},
	{1, arcs_40_10},
	{1, arcs_40_11},
	{2, arcs_40_12},
};
static arc arcs_41_0[1] = {
	{99, 1},
};
static arc arcs_41_1[1] = {
	{24, 2},
};
static arc arcs_41_2[2] = {
	{100, 3},
	{25, 4},
};
static arc arcs_41_3[1] = {
	{25, 4},
};
static arc arcs_41_4[1] = {
	{26, 5},
};
static arc arcs_41_5[1] = {
	{0, 5},
};
static state states_41[6] = {
	{1, arcs_41_0},
	{1, arcs_41_1},
	{2, arcs_41_2},
	{1, arcs_41_3},
	{1, arcs_41_4},
	{1, arcs_41_5},
};
static arc arcs_42_0[1] = {
	{80, 1},
};
static arc arcs_42_1[1] = {
	{101, 2},
};
static arc arcs_42_2[1] = {
	{0, 2},
};
static state states_42[3] = {
	{1, arcs_42_0},
	{1, arcs_42_1},
	{1, arcs_42_2},
};
static arc arcs_43_0[1] = {
	{102, 1},
};
static arc arcs_43_1[2] = {
	{24, 2},
	{0, 1},
};
static arc arcs_43_2[2] = {
	{80, 3},
	{0, 2},
};
static arc arcs_43_3[1] = {
	{21, 4},
};
static arc arcs_43_4[1] = {
	{0, 4},
};
static state states_43[5] = {
	{1, arcs_43_0},
	{2, arcs_43_1},
	{2, arcs_43_2},
	{1, arcs_43_3},
	{1, arcs_43_4},
};
static arc arcs_44_0[2] = {
	{3, 1},
	{2, 2},
};
static arc arcs_44_1[1] = {
	{0, 1},
};
static arc arcs_44_2[1] = {
	{103, 3},
};
static arc arcs_44_3[1] = {
	{6, 4},
};
static arc arcs_44_4[2] = {
	{6, 4},
	{104, 1},
};
static state states_44[5] = {
	{2, arcs_44_0},
	{1, arcs_44_1},
	{1, arcs_44_2},
	{1, arcs_44_3},
	{2, arcs_44_4},
};
static arc arcs_45_0[2] = {
	{105, 1},
	{106, 2},
};
static arc arcs_45_1[2] = {
	{90, 3},
	{0, 1},
};
static arc arcs_45_2[1] = {
	{0, 2},
};
static arc arcs_45_3[1] = {
	{105, 4},
};
static arc arcs_45_4[1] = {
	{92, 5},
};
static arc arcs_45_5[1] = {
	{24, 2},
};
static state states_45[6] = {
	{2, arcs_45_0},
	{2, arcs_45_1},
	{1, arcs_45_2},
	{1, arcs_45_3},
	{1, arcs_45_4},
	{1, arcs_45_5},
};
static arc arcs_46_0[2] = {
	{105, 1},
	{108, 1},
};
static arc arcs_46_1[1] = {
	{0, 1},
};
static state states_46[2] = {
	{2, arcs_46_0},
	{1, arcs_46_1},
};
static arc arcs_47_0[1] = {
	{109, 1},
};
static arc arcs_47_1[2] = {
	{33, 2},
	{25, 3},
};
static arc arcs_47_2[1] = {
	{25, 3},
};
static arc arcs_47_3[1] = {
	{24, 4},
};
static arc arcs_47_4[1] = {
	{0, 4},
};
static state states_47[5] = {
	{1, arcs_47_0},
	{2, arcs_47_1},
	{1, arcs_47_2},
	{1, arcs_47_3},
	{1, arcs_47_4},
};
static arc arcs_48_0[1] = {
	{109, 1},
};
static arc arcs_48_1[2] = {
	{33, 2},
	{25, 3},
};
static arc arcs_48_2[1] = {
	{25, 3},
};
static arc arcs_48_3[1] = {
	{107, 4},
};
static arc arcs_48_4[1] = {
	{0, 4},
};
static state states_48[5] = {
	{1, arcs_48_0},
	{2, arcs_48_1},
	{1, arcs_48_2},
	{1, arcs_48_3},
	{1, arcs_48_4},
};
static arc arcs_49_0[1] = {
	{110, 1},
};
static arc arcs_49_1[2] = {
	{111, 0},
	{0, 1},
};
static state states_49[2] = {
	{1, arcs_49_0},
	{2, arcs_49_1},
};
static arc arcs_50_0[1] = {
	{112, 1},
};
static arc arcs_50_1[2] = {
	{113, 0},
	{0, 1},
};
static state states_50[2] = {
	{1, arcs_50_0},
	{2, arcs_50_1},
};
static arc arcs_51_0[2] = {
	{114, 1},
	{115, 2},
};
static arc arcs_51_1[1] = {
	{112, 2},
};
static arc arcs_51_2[1] = {
	{0, 2},
};
static state states_51[3] = {
	{2, arcs_51_0},
	{1, arcs_51_1},
	{1, arcs_51_2},
};
static arc arcs_52_0[1] = {
	{116, 1},
};
static arc arcs_52_1[2] = {
	{117, 0},
	{0, 1},
};
static state states_52[2] = {
	{1, arcs_52_0},
	{2, arcs_52_1},
};
static arc arcs_53_0[9] = {
	{118, 1},
	{119, 1},
	{120, 1},
	{121, 1},
	{122, 1},
	{123, 1},
	{95, 1},
	{114, 2},
	{124, 3},
};
static arc arcs_53_1[1] = {
	{0, 1},
};
static arc arcs_53_2[1] = {
	{95, 1},
};
static arc arcs_53_3[2] = {
	{114, 1},
	{0, 3},
};
static state states_53[4] = {
	{9, arcs_53_0},
	{1, arcs_53_1},
	{1, arcs_53_2},
	{2, arcs_53_3},
};
static arc arcs_54_0[2] = {
	{31, 1},
	{101, 2},
};
static arc arcs_54_1[1] = {
	{101, 2},
};
static arc arcs_54_2[1] = {
	{0, 2},
};
static state states_54[3] = {
	{2, arcs_54_0},
	{1, arcs_54_1},
	{1, arcs_54_2},
};
static arc arcs_55_0[1] = {
	{125, 1},
};
static arc arcs_55_1[2] = {
	{126, 0},
	{0, 1},
};
static state states_55[2] = {
	{1, arcs_55_0},
	{2, arcs_55_1},
};
static arc arcs_56_0[1] = {
	{127, 1},
};
static arc arcs_56_1[2] = {
	{128, 0},
	{0, 1},
};
static state states_56[2] = {
	{1, arcs_56_0},
	{2, arcs_56_1},
};
static arc arcs_57_0[1] = {
	{129, 1},
};
static arc arcs_57_1[2] = {
	{130, 0},
	{0, 1},
};
static state states_57[2] = {
	{1, arcs_57_0},
	{2, arcs_57_1},
};
static arc arcs_58_0[1] = {
	{131, 1},
};
static arc arcs_58_1[3] = {
	{132, 0},
	{133, 0},
	{0, 1},
};
static state states_58[2] = {
	{1, arcs_58_0},
	{3, arcs_58_1},
};
static arc arcs_59_0[1] = {
	{134, 1},
};
static arc arcs_59_1[3] = {
	{135, 0},
	{136, 0},
	{0, 1},
};
static state states_59[2] = {
	{1, arcs_59_0},
	{3, arcs_59_1},
};
static arc arcs_60_0[1] = {
	{137, 1},
};
static arc arcs_60_1[5] = {
	{31, 0},
	{138, 0},
	{139, 0},
	{140, 0},
	{0, 1},
};
static state states_60[2] = {
	{1, arcs_60_0},
	{5, arcs_60_1},
};
static arc arcs_61_0[4] = {
	{135, 1},
	{136, 1},
	{141, 1},
	{142, 2},
};
static arc arcs_61_1[1] = {
	{137, 2},
};
static arc arcs_61_2[1] = {
	{0, 2},
};
static state states_61[3] = {
	{4, arcs_61_0},
	{1, arcs_61_1},
	{1, arcs_61_2},
};
static arc arcs_62_0[1] = {
	{143, 1},
};
static arc arcs_62_1[3] = {
	{144, 1},
	{32, 2},
	{0, 1},
};
static arc arcs_62_2[1] = {
	{137, 3},
};
static arc arcs_62_3[1] = {
	{0, 3},
};
static state states_62[4] = {
	{1, arcs_62_0},
	{3, arcs_62_1},
	{1, arcs_62_2},
	{1, arcs_62_3},
};
static arc arcs_63_0[10] = {
	{13, 1},
	{146, 2},
	{148, 3},
	{21, 4},
	{151, 4},
	{152, 5},
	{77, 4},
	{153, 4},
	{154, 4},
	{155, 4},
};
static arc arcs_63_1[3] = {
	{46, 6},
	{145, 6},
	{15, 4},
};
static arc arcs_63_2[2] = {
	{145, 7},
	{147, 4},
};
static arc arcs_63_3[2] = {
	{149, 8},
	{150, 4},
};
static arc arcs_63_4[1] = {
	{0, 4},
};
static arc arcs_63_5[2] = {
	{152, 5},
	{0, 5},
};
static arc arcs_63_6[1] = {
	{15, 4},
};
static arc arcs_63_7[1] = {
	{147, 4},
};
static arc arcs_63_8[1] = {
	{150, 4},
};
static state states_63[9] = {
	{10, arcs_63_0},
	{3, arcs_63_1},
	{2, arcs_63_2},
	{2, arcs_63_3},
	{1, arcs_63_4},
	{2, arcs_63_5},
	{1, arcs_63_6},
	{1, arcs_63_7},
	{1, arcs_63_8},
};
static arc arcs_64_0[1] = {
	{24, 1},
};
static arc arcs_64_1[3] = {
	{156, 2},
	{30, 3},
	{0, 1},
};
static arc arcs_64_2[1] = {
	{0, 2},
};
static arc arcs_64_3[2] = {
	{24, 4},
	{0, 3},
};
static arc arcs_64_4[2] = {
	{30, 3},
	{0, 4},
};
static state states_64[5] = {
	{1, arcs_64_0},
	{3, arcs_64_1},
	{1, arcs_64_2},
	{2, arcs_64_3},
	{2, arcs_64_4},
};
static arc arcs_65_0[3] = {
	{13, 1},
	{146, 2},
	{76, 3},
};
static arc arcs_65_1[2] = {
	{14, 4},
	{15, 5},
};
static arc arcs_65_2[1] = {
	{157, 6},
};
static arc arcs_65_3[1] = {
	{21, 5},
};
static arc arcs_65_4[1] = {
	{15, 5},
};
static arc arcs_65_5[1] = {
	{0, 5},
};
static arc arcs_65_6[1] = {
	{147, 5},
};
static state states_65[7] = {
	{3, arcs_65_0},
	{2, arcs_65_1},
	{1, arcs_65_2},
	{1, arcs_65_3},
	{1, arcs_65_4},
	{1, arcs_65_5},
	{1, arcs_65_6},
};
static arc arcs_66_0[1] = {
	{158, 1},
};
static arc arcs_66_1[2] = {
	{30, 2},
	{0, 1},
};
static arc arcs_66_2[2] = {
	{158, 1},
	{0, 2},
};
static state states_66[3] = {
	{1, arcs_66_0},
	{2, arcs_66_1},
	{2, arcs_66_2},
};
static arc arcs_67_0[2] = {
	{24, 1},
	{25, 2},
};
static arc arcs_67_1[2] = {
	{25, 2},
	{0, 1},
};
static arc arcs_67_2[3] = {
	{24, 3},
	{159, 4},
	{0, 2},
};
static arc arcs_67_3[2] = {
	{159, 4},
	{0, 3},
};
static arc arcs_67_4[1] = {
	{0, 4},
};
static state states_67[5] = {
	{2, arcs_67_0},
	{2, arcs_67_1},
	{3, arcs_67_2},
	{2, arcs_67_3},
	{1, arcs_67_4},
};
static arc arcs_68_0[1] = {
	{25, 1},
};
static arc arcs_68_1[2] = {
	{24, 2},
	{0, 1},
};
static arc arcs_68_2[1] = {
	{0, 2},
};
static state states_68[3] = {
	{1, arcs_68_0},
	{2, arcs_68_1},
	{1, arcs_68_2},
};
static arc arcs_69_0[1] = {
	{116, 1},
};
static arc arcs_69_1[2] = {
	{30, 2},
	{0, 1},
};
static arc arcs_69_2[2] = {
	{116, 1},
	{0, 2},
};
static state states_69[3] = {
	{1, arcs_69_0},
	{2, arcs_69_1},
	{2, arcs_69_2},
};
static arc arcs_70_0[1] = {
	{24, 1},
};
static arc arcs_70_1[2] = {
	{30, 2},
	{0, 1},
};
static arc arcs_70_2[2] = {
	{24, 1},
	{0, 2},
};
static state states_70[3] = {
	{1, arcs_70_0},
	{2, arcs_70_1},
	{2, arcs_70_2},
};
static arc arcs_71_0[1] = {
	{24, 1},
};
static arc arcs_71_1[4] = {
	{25, 2},
	{156, 3},
	{30, 4},
	{0, 1},
};
static arc arcs_71_2[1] = {
	{24, 5},
};
static arc arcs_71_3[1] = {
	{0, 3},
};
static arc arcs_71_4[2] = {
	{24, 6},
	{0, 4},
};
static arc arcs_71_5[3] = {
	{156, 3},
	{30, 7},
	{0, 5},
};
static arc arcs_71_6[2] = {
	{30, 4},
	{0, 6},
};
static arc arcs_71_7[2] = {
	{24, 8},
	{0, 7},
};
static arc arcs_71_8[1] = {
	{25, 9},
};
static arc arcs_71_9[1] = {
	{24, 10},
};
static arc arcs_71_10[2] = {
	{30, 7},
	{0, 10},
};
static state states_71[11] = {
	{1, arcs_71_0},
	{4, arcs_71_1},
	{1, arcs_71_2},
	{1, arcs_71_3},
	{2, arcs_71_4},
	{3, arcs_71_5},
	{2, arcs_71_6},
	{2, arcs_71_7},
	{1, arcs_71_8},
	{1, arcs_71_9},
	{2, arcs_71_10},
};
static arc arcs_72_0[1] = {
	{160, 1},
};
static arc arcs_72_1[1] = {
	{21, 2},
};
static arc arcs_72_2[2] = {
	{13, 3},
	{25, 4},
};
static arc arcs_72_3[2] = {
	{14, 5},
	{15, 6},
};
static arc arcs_72_4[1] = {
	{26, 7},
};
static arc arcs_72_5[1] = {
	{15, 6},
};
static arc arcs_72_6[1] = {
	{25, 4},
};
static arc arcs_72_7[1] = {
	{0, 7},
};
static state states_72[8] = {
	{1, arcs_72_0},
	{1, arcs_72_1},
	{2, arcs_72_2},
	{2, arcs_72_3},
	{1, arcs_72_4},
	{1, arcs_72_5},
	{1, arcs_72_6},
	{1, arcs_72_7},
};
static arc arcs_73_0[3] = {
	{161, 1},
	{31, 2},
	{32, 3},
};
static arc arcs_73_1[2] = {
	{30, 4},
	{0, 1},
};
static arc arcs_73_2[1] = {
	{24, 5},
};
static arc arcs_73_3[1] = {
	{24, 6},
};
static arc arcs_73_4[4] = {
	{161, 1},
	{31, 2},
	{32, 3},
	{0, 4},
};
static arc arcs_73_5[2] = {
	{30, 7},
	{0, 5},
};
static arc arcs_73_6[1] = {
	{0, 6},
};
static arc arcs_73_7[1] = {
	{32, 3},
};
static state states_73[8] = {
	{3, arcs_73_0},
	{2, arcs_73_1},
	{1, arcs_73_2},
	{1, arcs_73_3},
	{4, arcs_73_4},
	{2, arcs_73_5},
	{1, arcs_73_6},
	{1, arcs_73_7},
};
static arc arcs_74_0[1] = {
	{24, 1},
};
static arc arcs_74_1[3] = {
	{156, 2},
	{29, 3},
	{0, 1},
};
static arc arcs_74_2[1] = {
	{0, 2},
};
static arc arcs_74_3[1] = {
	{24, 2},
};
static state states_74[4] = {
	{1, arcs_74_0},
	{3, arcs_74_1},
	{1, arcs_74_2},
	{1, arcs_74_3},
};
static arc arcs_75_0[2] = {
	{156, 1},
	{163, 1},
};
static arc arcs_75_1[1] = {
	{0, 1},
};
static state states_75[2] = {
	{2, arcs_75_0},
	{1, arcs_75_1},
};
static arc arcs_76_0[1] = {
	{94, 1},
};
static arc arcs_76_1[1] = {
	{60, 2},
};
static arc arcs_76_2[1] = {
	{95, 3},
};
static arc arcs_76_3[1] = {
	{105, 4},
};
static arc arcs_76_4[2] = {
	{162, 5},
	{0, 4},
};
static arc arcs_76_5[1] = {
	{0, 5},
};
static state states_76[6] = {
	{1, arcs_76_0},
	{1, arcs_76_1},
	{1, arcs_76_2},
	{1, arcs_76_3},
	{2, arcs_76_4},
	{1, arcs_76_5},
};
static arc arcs_77_0[1] = {
	{90, 1},
};
static arc arcs_77_1[1] = {
	{107, 2},
};
static arc arcs_77_2[2] = {
	{162, 3},
	{0, 2},
};
static arc arcs_77_3[1] = {
	{0, 3},
};
static state states_77[4] = {
	{1, arcs_77_0},
	{1, arcs_77_1},
	{2, arcs_77_2},
	{1, arcs_77_3},
};
static arc arcs_78_0[1] = {
	{24, 1},
};
static arc arcs_78_1[2] = {
	{30, 0},
	{0, 1},
};
static state states_78[2] = {
	{1, arcs_78_0},
	{2, arcs_78_1},
};
static arc arcs_79_0[1] = {
	{21, 1},
};
static arc arcs_79_1[1] = {
	{0, 1},
};
static state states_79[2] = {
	{1, arcs_79_0},
	{1, arcs_79_1},
};
static arc arcs_80_0[1] = {
	{166, 1},
};
static arc arcs_80_1[2] = {
	{9, 2},
	{0, 1},
};
static arc arcs_80_2[1] = {
	{0, 2},
};
static state states_80[3] = {
	{1, arcs_80_0},
	{2, arcs_80_1},
	{1, arcs_80_2},
};
static dfa dfas[81] = {
	{256, "single_input", 0, 3, states_0,
	 "\004\050\060\200\000\000\000\050\370\044\034\144\011\040\004\000\200\041\224\017\101"},
	{257, "file_input", 0, 2, states_1,
	 "\204\050\060\200\000\000\000\050\370\044\034\144\011\040\004\000\200\041\224\017\101"},
	{258, "eval_input", 0, 3, states_2,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{259, "decorator", 0, 7, states_3,
	 "\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{260, "decorators", 0, 2, states_4,
	 "\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{261, "decorated", 0, 3, states_5,
	 "\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{262, "funcdef", 0, 8, states_6,
	 "\000\000\020\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{263, "parameters", 0, 4, states_7,
	 "\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{264, "typedargslist", 0, 12, states_8,
	 "\000\000\040\200\001\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{265, "tfpdef", 0, 4, states_9,
	 "\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{266, "varargslist", 0, 12, states_10,
	 "\000\000\040\200\001\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{267, "vfpdef", 0, 2, states_11,
	 "\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{268, "stmt", 0, 2, states_12,
	 "\000\050\060\200\000\000\000\050\370\044\034\144\011\040\004\000\200\041\224\017\101"},
	{269, "simple_stmt", 0, 4, states_13,
	 "\000\040\040\200\000\000\000\050\370\044\034\000\000\040\004\000\200\041\224\017\100"},
	{270, "small_stmt", 0, 2, states_14,
	 "\000\040\040\200\000\000\000\050\370\044\034\000\000\040\004\000\200\041\224\017\100"},
	{271, "expr_stmt", 0, 6, states_15,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{272, "augassign", 0, 2, states_16,
	 "\000\000\000\000\000\200\377\007\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{273, "del_stmt", 0, 3, states_17,
	 "\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{274, "pass_stmt", 0, 2, states_18,
	 "\000\000\000\000\000\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{275, "flow_stmt", 0, 2, states_19,
	 "\000\000\000\000\000\000\000\000\170\000\000\000\000\000\000\000\000\000\000\000\100"},
	{276, "break_stmt", 0, 2, states_20,
	 "\000\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000"},
	{277, "continue_stmt", 0, 2, states_21,
	 "\000\000\000\000\000\000\000\000\020\000\000\000\000\000\000\000\000\000\000\000\000"},
	{278, "return_stmt", 0, 3, states_22,
	 "\000\000\000\000\000\000\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000"},
	{279, "yield_stmt", 0, 2, states_23,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\100"},
	{280, "raise_stmt", 0, 5, states_24,
	 "\000\000\000\000\000\000\000\000\100\000\000\000\000\000\000\000\000\000\000\000\000"},
	{281, "import_stmt", 0, 2, states_25,
	 "\000\000\000\000\000\000\000\000\200\004\000\000\000\000\000\000\000\000\000\000\000"},
	{282, "import_name", 0, 3, states_26,
	 "\000\000\000\000\000\000\000\000\000\004\000\000\000\000\000\000\000\000\000\000\000"},
	{283, "import_from", 0, 8, states_27,
	 "\000\000\000\000\000\000\000\000\200\000\000\000\000\000\000\000\000\000\000\000\000"},
	{284, "import_as_name", 0, 4, states_28,
	 "\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{285, "dotted_as_name", 0, 4, states_29,
	 "\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{286, "import_as_names", 0, 3, states_30,
	 "\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{287, "dotted_as_names", 0, 2, states_31,
	 "\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{288, "dotted_name", 0, 2, states_32,
	 "\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{289, "global_stmt", 0, 3, states_33,
	 "\000\000\000\000\000\000\000\000\000\000\004\000\000\000\000\000\000\000\000\000\000"},
	{290, "nonlocal_stmt", 0, 3, states_34,
	 "\000\000\000\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000\000\000"},
	{291, "assert_stmt", 0, 5, states_35,
	 "\000\000\000\000\000\000\000\000\000\000\020\000\000\000\000\000\000\000\000\000\000"},
	{292, "compound_stmt", 0, 2, states_36,
	 "\000\010\020\000\000\000\000\000\000\000\000\144\011\000\000\000\000\000\000\000\001"},
	{293, "if_stmt", 0, 8, states_37,
	 "\000\000\000\000\000\000\000\000\000\000\000\004\000\000\000\000\000\000\000\000\000"},
	{294, "while_stmt", 0, 8, states_38,
	 "\000\000\000\000\000\000\000\000\000\000\000\040\000\000\000\000\000\000\000\000\000"},
	{295, "for_stmt", 0, 10, states_39,
	 "\000\000\000\000\000\000\000\000\000\000\000\100\000\000\000\000\000\000\000\000\000"},
	{296, "try_stmt", 0, 13, states_40,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\001\000\000\000\000\000\000\000\000"},
	{297, "with_stmt", 0, 6, states_41,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000"},
	{298, "with_var", 0, 3, states_42,
	 "\000\000\000\000\000\000\000\000\000\000\001\000\000\000\000\000\000\000\000\000\000"},
	{299, "except_clause", 0, 5, states_43,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\100\000\000\000\000\000\000\000\000"},
	{300, "suite", 0, 5, states_44,
	 "\004\040\040\200\000\000\000\050\370\044\034\000\000\040\004\000\200\041\224\017\100"},
	{301, "test", 0, 6, states_45,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{302, "test_nocond", 0, 2, states_46,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{303, "lambdef", 0, 5, states_47,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\040\000\000\000\000\000\000\000"},
	{304, "lambdef_nocond", 0, 5, states_48,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\040\000\000\000\000\000\000\000"},
	{305, "or_test", 0, 2, states_49,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\000\004\000\200\041\224\017\000"},
	{306, "and_test", 0, 2, states_50,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\000\004\000\200\041\224\017\000"},
	{307, "not_test", 0, 3, states_51,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\000\004\000\200\041\224\017\000"},
	{308, "comparison", 0, 2, states_52,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\000\000\000\200\041\224\017\000"},
	{309, "comp_op", 0, 4, states_53,
	 "\000\000\000\000\000\000\000\000\000\000\000\200\000\000\304\037\000\000\000\000\000"},
	{310, "star_expr", 0, 3, states_54,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\000\000\000\200\041\224\017\000"},
	{311, "expr", 0, 2, states_55,
	 "\000\040\040\000\000\000\000\000\000\040\000\000\000\000\000\000\200\041\224\017\000"},
	{312, "xor_expr", 0, 2, states_56,
	 "\000\040\040\000\000\000\000\000\000\040\000\000\000\000\000\000\200\041\224\017\000"},
	{313, "and_expr", 0, 2, states_57,
	 "\000\040\040\000\000\000\000\000\000\040\000\000\000\000\000\000\200\041\224\017\000"},
	{314, "shift_expr", 0, 2, states_58,
	 "\000\040\040\000\000\000\000\000\000\040\000\000\000\000\000\000\200\041\224\017\000"},
	{315, "arith_expr", 0, 2, states_59,
	 "\000\040\040\000\000\000\000\000\000\040\000\000\000\000\000\000\200\041\224\017\000"},
	{316, "term", 0, 2, states_60,
	 "\000\040\040\000\000\000\000\000\000\040\000\000\000\000\000\000\200\041\224\017\000"},
	{317, "factor", 0, 3, states_61,
	 "\000\040\040\000\000\000\000\000\000\040\000\000\000\000\000\000\200\041\224\017\000"},
	{318, "power", 0, 4, states_62,
	 "\000\040\040\000\000\000\000\000\000\040\000\000\000\000\000\000\000\000\224\017\000"},
	{319, "atom", 0, 9, states_63,
	 "\000\040\040\000\000\000\000\000\000\040\000\000\000\000\000\000\000\000\224\017\000"},
	{320, "testlist_comp", 0, 5, states_64,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{321, "trailer", 0, 7, states_65,
	 "\000\040\000\000\000\000\000\000\000\020\000\000\000\000\000\000\000\000\004\000\000"},
	{322, "subscriptlist", 0, 3, states_66,
	 "\000\040\040\202\000\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{323, "subscript", 0, 5, states_67,
	 "\000\040\040\202\000\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{324, "sliceop", 0, 3, states_68,
	 "\000\000\000\002\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{325, "exprlist", 0, 3, states_69,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\000\000\000\200\041\224\017\000"},
	{326, "testlist", 0, 3, states_70,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{327, "dictorsetmaker", 0, 11, states_71,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{328, "classdef", 0, 8, states_72,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\001"},
	{329, "arglist", 0, 8, states_73,
	 "\000\040\040\200\001\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{330, "argument", 0, 4, states_74,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{331, "comp_iter", 0, 2, states_75,
	 "\000\000\000\000\000\000\000\000\000\000\000\104\000\000\000\000\000\000\000\000\000"},
	{332, "comp_for", 0, 6, states_76,
	 "\000\000\000\000\000\000\000\000\000\000\000\100\000\000\000\000\000\000\000\000\000"},
	{333, "comp_if", 0, 4, states_77,
	 "\000\000\000\000\000\000\000\000\000\000\000\004\000\000\000\000\000\000\000\000\000"},
	{334, "testlist1", 0, 2, states_78,
	 "\000\040\040\200\000\000\000\000\000\040\000\000\000\040\004\000\200\041\224\017\000"},
	{335, "encoding_decl", 0, 2, states_79,
	 "\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{336, "yield_expr", 0, 3, states_80,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\100"},
};
static label labels[167] = {
	{0, "EMPTY"},
	{256, 0},
	{4, 0},
	{269, 0},
	{292, 0},
	{257, 0},
	{268, 0},
	{0, 0},
	{258, 0},
	{326, 0},
	{259, 0},
	{50, 0},
	{288, 0},
	{7, 0},
	{329, 0},
	{8, 0},
	{260, 0},
	{261, 0},
	{328, 0},
	{262, 0},
	{1, "def"},
	{1, 0},
	{263, 0},
	{51, 0},
	{301, 0},
	{11, 0},
	{300, 0},
	{264, 0},
	{265, 0},
	{22, 0},
	{12, 0},
	{16, 0},
	{36, 0},
	{266, 0},
	{267, 0},
	{270, 0},
	{13, 0},
	{271, 0},
	{273, 0},
	{274, 0},
	{275, 0},
	{281, 0},
	{289, 0},
	{290, 0},
	{291, 0},
	{272, 0},
	{336, 0},
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
	{1, "del"},
	{325, 0},
	{1, "pass"},
	{276, 0},
	{277, 0},
	{278, 0},
	{280, 0},
	{279, 0},
	{1, "break"},
	{1, "continue"},
	{1, "return"},
	{1, "raise"},
	{1, "from"},
	{282, 0},
	{283, 0},
	{1, "import"},
	{287, 0},
	{23, 0},
	{52, 0},
	{286, 0},
	{284, 0},
	{1, "as"},
	{285, 0},
	{1, "global"},
	{1, "nonlocal"},
	{1, "assert"},
	{293, 0},
	{294, 0},
	{295, 0},
	{296, 0},
	{297, 0},
	{1, "if"},
	{1, "elif"},
	{1, "else"},
	{1, "while"},
	{1, "for"},
	{1, "in"},
	{1, "try"},
	{299, 0},
	{1, "finally"},
	{1, "with"},
	{298, 0},
	{311, 0},
	{1, "except"},
	{5, 0},
	{6, 0},
	{305, 0},
	{303, 0},
	{302, 0},
	{304, 0},
	{1, "lambda"},
	{306, 0},
	{1, "or"},
	{307, 0},
	{1, "and"},
	{1, "not"},
	{308, 0},
	{310, 0},
	{309, 0},
	{20, 0},
	{21, 0},
	{28, 0},
	{31, 0},
	{30, 0},
	{29, 0},
	{1, "is"},
	{312, 0},
	{18, 0},
	{313, 0},
	{33, 0},
	{314, 0},
	{19, 0},
	{315, 0},
	{34, 0},
	{35, 0},
	{316, 0},
	{14, 0},
	{15, 0},
	{317, 0},
	{17, 0},
	{24, 0},
	{48, 0},
	{32, 0},
	{318, 0},
	{319, 0},
	{321, 0},
	{320, 0},
	{9, 0},
	{10, 0},
	{26, 0},
	{327, 0},
	{27, 0},
	{2, 0},
	{3, 0},
	{1, "None"},
	{1, "True"},
	{1, "False"},
	{332, 0},
	{322, 0},
	{323, 0},
	{324, 0},
	{1, "class"},
	{330, 0},
	{331, 0},
	{333, 0},
	{334, 0},
	{335, 0},
	{1, "yield"},
};
grammar _PyParser_Grammar = {
	81,
	dfas,
	{167, labels},
	256
};
