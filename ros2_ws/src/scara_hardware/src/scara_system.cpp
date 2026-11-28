#include "scara_hardware/scara_system.hpp"
#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "rclcpp/rclcpp.hpp"

#include <sstream>
#include <string>

namespace scara_hardware {

    hardware_interface::CallbackReturn ScaraSystem::on_init(
        const hardware_interface::HardwareComponentsInterfaceParams & params){
            if(
                hardware_interface::SystemInterface::on_init(params) !=
                hardware_interface::CallbackReturn::SUCCESS)
            {
                return hardware_interface::CallbackReturn::ERROR;
            }

            for(const hardware_interface::ComponentInfo & joint : info_.joints)
            {
                if(
                    joint.command_interfaces.size() != 1 ||
                    joint.command_interfaces[0].name != hardware_interface::HW_IF_POSITION)
                {
                    RCLCPP_FATAL(
                        get_logger(), "Joint '%s': expected exactly one command interface '%s'.",
                        joint.name.c_str(), hardware_interface::HW_IF_POSITION);
                    return hardware_interface::CallbackReturn::ERROR;
                }

                if(
                    joint.state_interfaces.size() != 1 ||
                    joint.state_interfaces[0].name != hardware_interface::HW_IF_POSITION)
                {
                    RCLCPP_FATAL(
                        get_logger(), "Joint '%s': expected exactly one state interface '%s'.",
                        joint.name.c_str(), hardware_interface::HW_IF_POSITION);
                    return hardware_interface::CallbackReturn::ERROR;
                }
            }

            RCLCPP_INFO(get_logger(), "on_init OK, joints: %zu", info_.joints_size());
            return hardware_interface::CallbackReturn::SUCCESS;
        }

    hardware_interface::CallbackReturn ScaraSystem::on_configure(
        const rclcpp_lifecycle::State & /*previous_state*/){
            for(const auto & [name, descr] : joint_state_interfaces_)
            {
                set_state(name, 0.0);
            }
            for(const auto & [name, descr]: joint_command_interfaces_)
            {
                set_command(name, 0.0);
            }
            RCLCPP_INFO(get_logger(), "on_configure OK");
            return hardware_interface::CallbackReturn::SUCCESS;
        }

    hardware_interface::CallbackReturn ScaraSystem::on_activate(
        const rclcpp_lifecycle::State & /*previous_state*/){
            for(const auto & [name, descr] : joint_state_interfaces_)
            {
                set_command(name, get_state(name));
            }
            RCLCPP_INFO(get_logger(), "on_activate OK");
            return hardware_interface::CallbackReturn::SUCCESS;
        }

    hardware_interface::CallbackReturn on_deactivate(
        const rclcpp_lifecycle::State & /*previous_state*/){
            
            RCLCPP_INFO(get_logger(), "on_deactivate OK");
            return hardware_interface::CallbackReturn::SUCCESS;
        }
    
    hardware_interface::return_type read(
        const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/){
            std::stringstream ss;
            ss << "read():";

            for(const auto & [name, descr] : joint_state_intefaces_)
            {
                set_state(name, get_command(name));
                ss << "\n\t" << name << "=" << get_state(name);
            }
            RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), 1000, "%s", ss.str().c_str());
            return hardware_interface::return_type::OK;
        }

    hardware_interface::return_type write(
        const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/){
            std::stringstream ss;
            ss << "write():";

            for(const auto & [name, descr] : joint_state_interfaces_)
            {
                ss << "\n\t" << name << "<-" << get_command(name);
            }
            RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), 1000, "%s", ss.str().c_str());
            return hardware_interface::return_type::OK;
        }

}

#include "pluginlib/class_list_macros.hpp"

PLUGINLIB_EXPORT_CLASS(scara_hardware::ScaraSystem, hardware_interface::SystemInterface)