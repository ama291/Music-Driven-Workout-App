//
//  ViewModel.swift
//  Music-Driven-Workout-App
//
//  Created by Lucy Newman on 2/28/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

//import UIKit
//
//class ViewModel: NSObject {
//    var items = [ViewModelItem]()
//    
//}
//
//extension ViewModel: UITableViewDataSource {
//    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
//        return items.count
//    }
//    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
//        if let cell = tableView.dequeueReusableCell(withIdentifier: TrackedExTableViewCell.identifier, for: indexPath) as TrackedExTableViewCell {
//            cell.item = items[indexPath.row]
//            
//            if items[indexPath.row].isSelected {
//                tableView.selectRow(at: indexPath, animated: false, scrollPosition: .none)
//            } else {
//                tableView.deselectRow(at: indexPath, animated: false)
//            }
//            return cell
//        }
//        return UITableViewCell()
//    }
//
//}

