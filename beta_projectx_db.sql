/*
 Navicat Premium Data Transfer

 Source Server         : ProjectXConnection
 Source Server Type    : MySQL
 Source Server Version : 80032
 Source Host           : localhost:3306
 Source Schema         : beta_projectx_db

 Target Server Type    : MySQL
 Target Server Version : 80032
 File Encoding         : 65001

 Date: 13/10/2023 14:00:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `remember_token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'member', 'techguru', 'tech.guru.k.p@gmail.com', '$2b$12$pbG1essKV2lSb12Rny20/.V5Eaof2vrpywzBy3YPaOwBbEy5cVX4O', NULL, '2023-10-13 13:48:59', '2023-10-13 13:48:59', NULL);
INSERT INTO `users` VALUES (2, 'member', ' ', 'tch.guru.k.p@gmail.com', '$2b$12$DbwleggdmJXveCZVRIxLDO7XNyJvPY8GLl5T/97g15vFfzsZuG93a', NULL, '2023-10-13 13:49:27', '2023-10-13 13:59:12', NULL);
INSERT INTO `users` VALUES (3, 'member', 'crazydev', 'crazydev121213@gmail.com', '$2b$12$qE13Xg0ot/vIBcrLLusj.O/YxoK7izxRix7LkAPucZFO2ATuR7LKe', NULL, '2023-10-13 13:52:12', '2023-10-13 13:52:12', NULL);

SET FOREIGN_KEY_CHECKS = 1;
