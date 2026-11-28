#ifndef SCARA_PROJECT_SCARA_SYSTEM_HPP_
#define SCARA_PROJECT_SCARA_SYSTEM_HPP_

#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "rclcpp/macros.hpp"
#include "rclcpp_lifecycle/node_interfaces/lifecycle_node_interface.hpp"
#include "rclcpp_lifecycle/state.hpp"

namespace scara_hardware
{
    class ScaraSystem: public hardware_interface::SystemInterface
    {
    public:

        RCLCPP_SHARED_PTR_DEFINITNIONS(ScaraSystem)

        hardware_interface::CallbackReturn on_init( // hardware_interface::CallbackReturn is a type alias for rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn
            const hardware_interface::HardwareComponentsInterfaceParams & params) override;

        hardware_interface::CallbackReturn on_configure(
            const rclcpp_lifecycle::State & previous_state) override;

        hardware_interface::CallbackReturn on_activate(
            const rclcpp_lifecycle::State & previous_state) override;

        hardware_interface::CallbackReturn on_deactivate(
            const rclcpp_lifecycle::State & previous_state) override;

        hardware_interface::return_type read(
            const rclcpp::Time & time, const rclcpp::Duration & period) override;

        hardware_interface::return_type write(
            const rclcpp::Time & time, const rclcpp::Duration & period) override;

    };
}

#endif