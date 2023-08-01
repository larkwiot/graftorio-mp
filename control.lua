function write_tick(json)
    local filename = "graftoriomp_stats.json"
    game.write_file(filename, json .. "\n")
end

--@type LuaFlowStatistics
function get_prod_cons(production_statistics)
    local production = {}
    local consumption = {}

    for item, amount in pairs(production_statistics.input_counts) do
        production[item] = amount
    end

    for item, amount in pairs(production_statistics.output_counts) do
        consumption[item] = amount
    end

    return production, consumption
end

--@type LuaForce
function get_force_data(force)
    local item_production, item_consumption = get_prod_cons(force.item_production_statistics)

    local fluid_production, fluid_consumption = get_prod_cons(force.fluid_production_statistics)

    return {
        ["item_production"] = item_production,
        ["item_consumption"] = item_consumption,
        ["fluid_production"] = fluid_production,
        ["fluid_consumption"] = fluid_consumption,
    }
end

--type@NthTickEventData
function tick_handler(tick_event)
    local tick = tick_event.tick

    local data = { ["player"] = get_force_data(game.forces["player"]) }

    local json = game.table_to_json(data)

    write_tick(json)
end

-- 60 tps * 15 s
script.on_nth_tick(60*15, tick_handler)
